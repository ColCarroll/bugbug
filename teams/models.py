""" The Team class
"""
from django.db import models

class Team(models.Model):
  """ Data on an individual team
  """
  display_name = models.CharField(max_length = 100)
  meets = models.ManyToManyField('meets.Meet')

class TeamAlias(models.Model):
  """ Various spellings of team names
  """
  alias = models.CharField(max_length = 100)
  display_name = models.ForeignKey(Team)

