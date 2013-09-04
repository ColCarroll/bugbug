""" The Meet class
"""
from django.db import models

class Meet(models.Model):
  """ Carries individual meet information
  """
  city = models.CharField(max_length = 100)
  host_school = models.CharField(max_length = 100)
