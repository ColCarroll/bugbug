""" The Results class
"""
from django.db import models

class Result(models.Model):
  """ An individual meet result
  """
  meet = models.ForeignKey('meets.Meet')
  runner = models.ForeignKey('runners.Runner')
  time = models.TimeField()

