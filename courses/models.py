""" The Course class
"""
from django.db import models

class Course(models.Model):
  """ Handles course functions
  """
  host = models.CharField(max_length = 150)
  city = models.CharField(max_length = 150)
  state = models.CharField(max_length = 150)
  distance = models.CharField(max_length = 150)
