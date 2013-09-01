""" Create your views here.
"""
from django.http import HttpResponse

def homepage(request):
  """Home page for teams
  """
  return HttpResponse('<html><title>BugBug Teams</title></html>')

