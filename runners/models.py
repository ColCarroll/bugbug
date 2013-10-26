"""The Runner class
"""
from django.db import models

class Runner(models.Model):
  """ Data on an individual runner
  """
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  team = models.ForeignKey('teams.Team')
  class_year = models.IntegerField()

  def __repr__(self):
    return "{0.first_name:s} {0.last_name:s}".format(self)

  def __str__(self):
    return "{0.first_name:s} {0.last_name:s}".format(self)

  @property
  def gender(self):
    """ A method to access the runner's gender
    """
    return self.result_set.all()[0].meet.gender
