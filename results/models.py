""" The Results class
"""
from django.db import models
from django.db.models import Count


class Result(models.Model):
  """ An individual meet result
  """
  meet = models.ForeignKey('meets.Meet')
  time = models.FloatField()
  runner = models.ForeignKey('runners.Runner')

  @property
  def get_time(self):
    """Returns a formatted time
    """
    minutes, seconds = divmod(self.time, 60)
    return "{0:02.0f}:{1:04.1f}".format(minutes, seconds)

  @property
  def get_place(self):
    """Returns a place in the meet
    """
    return self.objects.filter(meet__pk = self.meet.pk).filter(time__lt = self.time).count()
