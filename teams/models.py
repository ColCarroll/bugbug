""" The Team class
"""
from django.db import models

class Team(models.Model):
  """ Data on an individual team
  """
  name = models.CharField(max_length = 100)

class TeamAlias(models.Model):
  """ Various spellings of team names
  """
  alias = models.CharField(max_length = 100)
  name = models.ForeignKey(Team)

