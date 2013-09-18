""" Search engines for elastic search
"""

from haystack import indexes
from runners.models import Runner

class RunnerIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True, use_template = True)

  def get_model(self):
    return Runner

  def index_queryset(self, using = None):
    """ Used when the entire index for model is updated
    """
    return self.get_model().objects.all()
