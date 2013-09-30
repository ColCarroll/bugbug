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
    return sorted(list(set(j.meet for
        j in sum([list(j.result_set.all()) for
          j in self.runner_set.all()],[]))),
        key = lambda j:j.date, reverse = True)

  @property
  def url(self):
    """
    A link to the team's home page
    """
    return "<a href=\"{% url 'teams.views.roster' self.pk %}\">{0:}</a>".format(self.name)

class TeamAlias(models.Model):
  """ Various spellings of team names
  """
  alias = models.CharField(max_length = 100)
  name = models.ForeignKey(Team)

