"""The Runner class
"""

from django.db import models

class Runner(models.Model):
  """ Data on an individual runner
  """
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  teams = models.ManyToManyField('teams.Team')
  class_year = models.IntegerField()
