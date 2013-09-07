""" The Results class
"""
from django.db import models

class Result(models.Model):
  """ An individual meet result
  """
  meet = models.ForeignKey('meets.Meet')
  time = models.TimeField()
  runner = models.ForeignKey('runners.Runner')

