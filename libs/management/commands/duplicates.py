__author__ = 'colinc'

import itertools
from collections import defaultdict
import pylev

from django.db import transaction
from django.db.models import get_models, Model
from django.contrib.contenttypes.generic import GenericForeignKey
from django.core.management.base import BaseCommand

from teams.models import Team
from runners.models import Runner


def levenshtein_ratio(str_one, str_two):
  """
  Levenshtein ratio
  """
  str_len = len(str_one + str_two)
  return (str_len - pylev.levenshtein(str_one, str_two)) / float(str_len)


def find_duplicate_teams():
  """
  Tries to intelligently identify different teams
  """
  teams = Team.objects.all()
  doubles = defaultdict(set)
  for team_tuple in itertools.combinations(teams, 2):
    if team_similarity(*team_tuple):
      ordered_tuple = sorted(
          team_tuple,
          key=lambda j: len(j.runner_set.all()))
      doubles[ordered_tuple[0].pk].add(ordered_tuple[1].pk)
  return dict(doubles)


def find_duplicate_runners():
  """
  Tries to find duplicate runners on the same team
  """
  teams = Team.objects.all()
  for j, team in enumerate(teams):
    print("Analyzing team {0:d} of {1:d}".format(j, len(teams)))
    doubles = defaultdict(set)
    for runner_tuple in itertools.combinations(team.runner_set.all(), 2):
      if runner_similarity(*runner_tuple):
        ordered_tuple = sorted(
            runner_tuple,
            key=lambda j: len(j.result_set.all())
        )
        doubles[ordered_tuple[0].pk].add(ordered_tuple[1].pk)
    doubles = combine_dict(dict(doubles))
    merge_duplicate_objects(doubles, 'runner')


def combine_dict(dupes):
  """
  Takes a dictionary of primary key: set(primary key),
  and returns list of disjoint sets.
  """
  all_sets = [[j[0]] + list(j[1]) for j in dupes.items()]
  sets = []
  for key in dupes:
    sets.append({key})
    old_len = 0
    while old_len != len(sets[-1]):
      old_len = len(sets[-1])
      for new_key in sets[-1]:
        sets[-1] = sets[-1].union(set(
            sum([j for j in all_sets if new_key in j], [])))
  sets = list(set([tuple(the_set) for the_set in sets]))
  return sets


def merge_duplicate_objects(dupes, object_type):
  """
  Accepts a list of tuples, looks them up in the team table, and merges
  the objects
  """
  for pks in dupes:
    if object_type == 'team':
      objects = Team.objects.filter(pk__in=pks)
      objects = sorted(
          objects,
          key=lambda j: len(j.runner_set.all()))
    elif object_type == 'runner':
      objects = Runner.objects.filter(pk__in=pks)
      objects = sorted(
          objects,
          key=lambda j:len(j.result_set.all())
      )
    merge_model_objects(objects[0], objects[1:])


def team_merge():
  """
  Wraps up all the team and runner merging functionality
  """
  team_dupes = find_duplicate_teams()
  team_dupes = combine_dict(team_dupes)
  merge_duplicate_objects(team_dupes, 'team')


def runner_similarity(runner_one, runner_two):
  """
  Scores similarity between two runners (assumes they are
  on the same team)
  """
  if set(runner_one.result_set.all()).intersection(
     set(runner_two.result_set.all())):
    return False

  if levenshtein_ratio(str(runner_one), str(runner_two)) < 0.9:
    return False

  try:
    if str(runner_one) != str(runner_two):
      print("Found {0} and {1} on {1.team}".format(runner_one, runner_two))
    else:
      print("Found a double of {0} on {1.team}".format(runner_one, runner_two))
  except UnicodeEncodeError:
    print('Unicode Error! Continuing...')
    pass
  return True


def team_similarity(team_one, team_two):
  """
  Scores a similarity between two teams
  """
  name_similarity = set(team_one.name.lower().split()).intersection(
      set(team_two.name.lower().split())
  )
  if len(name_similarity) == 0:
    return False

  common_runners = set(
      str(runner) for runner in team_one.runner_set.all()
  ).intersection(
      set(
          str(runner) for runner in team_two.runner_set.all()
      )
  )
  if len(common_runners) < 2:
    return False

  common_meets = set(
      meet.id for meet in team_one.meets
  ).intersection(
      set(
          meet.id for meet in team_two.meets))
  if len(common_meets) > 2:
    return False
  print("Same team!: {0:s} and {1:s}".format(str(team_one), str(team_two)))
  return True


@transaction.commit_on_success
def merge_model_objects(primary_object, alias_objects=None, keep_old=False):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.

    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """
    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]

    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__

    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')

    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError('Only models of same class can be merged')

    # Get a list of all GenericForeignKeys in all models
    generic_fields = []
    for model in get_models():
        for field_name, field in filter(lambda x: isinstance(
                x[1], GenericForeignKey), model.__dict__.items()):
            generic_fields.append(field)

    blank_local_fields = set([field.attname for
                              field in
                              primary_object._meta.local_fields if
                              getattr(primary_object, field.attname) in
                              [None, '']])

    # Loop through all alias objects and migrate their data to the
    # primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to
        # primary object.
        for related_object in alias_object._meta.get_all_related_objects():
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            related_objects = getattr(alias_object, alias_varname)
            for obj in related_objects.all():
                setattr(obj, obj_varname, primary_object)
                obj.save()

        # Migrate all many to many references from alias object to
        # primary object.
        for related_many_object in alias_object._meta.get_all_related_many_to_many_objects():
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name

            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()
            for obj in related_many_objects.all():
                getattr(obj, obj_varname).remove(alias_object)
                getattr(obj, obj_varname).add(primary_object)

        # Migrate all generic foreign key references from alias object to
        # primary object.
        for field in generic_fields:
            filter_kwargs = {field.fk_field: alias_object._get_pk_val(),
                             field.ct_field: field.get_content_type(
                             alias_object)}
            for generic_related_object in field.model.objects.filter(**filter_kwargs):
                setattr(generic_related_object, field.name, primary_object)
                generic_related_object.save()

        # Try to fill all missing values in primary object by values of
        # duplicates
        filled_up = set()
        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name)
            if val not in [None, '']:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        blank_local_fields -= filled_up

        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object


class Command(BaseCommand):
  help = "Cleans results in the database"

  def handle(self, *args, **options):
    team_merge()
    find_duplicate_runners()
