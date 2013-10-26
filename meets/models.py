""" The Meet class
"""
from django.db import models

class Meet(models.Model):
  """ Carries individual meet information
  """
  MALE = "Male"
  FEMALE = "Female"
  GENDER_CHOICES = (
      (MALE, MALE),
      (FEMALE, FEMALE),
      )

  gender = models.CharField(max_length = 6, choices = GENDER_CHOICES)
  meet_name = models.CharField(max_length = 240)
  date = models.DateField()
  course = models.ForeignKey('courses.Course')

  def __repr__(self):
    return "{0.date.year} {0.meet_name}".format(self)

  def __str__(self):
    return self.__repr__()
