""" Create your views here.
"""
from django.http import HttpResponse

def home_page(request):
  """Home page for teams
  """
  return HttpResponse('<html><title>BugBug</title></html>')
