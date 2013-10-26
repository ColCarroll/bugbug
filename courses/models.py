""" The Course class
"""
from django.db import models
from results.models import Result


class Course(models.Model):
  """ Handles course functions
  """
  host = models.CharField(max_length=150)
  city = models.CharField(max_length=150)
  state = models.CharField(max_length=150)
  distance = models.CharField(max_length=150)

  def __repr__(self):
    return "{0.host} in {0.city}, {0.state}".format(self)

  def __str__(self):
    return self.__repr__()

  def average_time(self, gender):
    """Returns the average time on the course
    """
    time = self.meet_set.filter(gender=gender).aggregate(models.Avg('result__time'))['result__time__avg']
    if time:
      return "{0:02.0f}:{1:04.1f}".format(*divmod(time,60))
    return "-"

  def women_average(self):
    """ Returns the average women's time
    """
    return self.average_time("Women")

  def men_average(self):
    """ Returns the average men's time
    """
    return self.average_time("Men")

  def record_result(self, gender):
    """Returns the result object with the record time for the course
    """
    min_time = self.meet_set.filter(gender=gender).aggregate(models.Min('result__time'))['result__time__min']
    if min_time:
      records = Result.objects.filter(meet__course__pk = self.pk, meet__gender = gender, time = min_time)
      if records:
        return records
    return None

  def women_record(self):
    """ Men's course record
    """
    return self.record_result("Women")

  def men_record(self):
    """ Men's course record
    """
    return self.record_result("Men")

