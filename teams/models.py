""" The Team class
"""
from django.db import models

class Team(models.Model):
  """ Data on an individual team
  """
  name = models.CharField(max_length = 100)

  @property
  def meets(self):
    """Returns a list of meets the teams' runners have
    participated in
    """
    return set(j.meet for
        j in sum([list(j.result_set.all()) for
          j in self.runner_set.all()],[]))

class TeamAlias(models.Model):
  """ Various spellings of team names
  """
  alias = models.CharField(max_length = 100)
  name = models.ForeignKey(Team)

