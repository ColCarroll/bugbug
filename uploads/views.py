""" Create your views here.
"""
from django.shortcuts import render

def homepage(request):
  """Home page for teams
  """
  return render(request, 'uploads/homepage.html')
