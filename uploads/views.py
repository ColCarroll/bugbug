""" Create your views here.
"""
import datetime
from django.shortcuts import render
from uploads.parser import Parser

def homepage(request):
  """Home page for teams
  """
  if request.method == "POST":
    parser = Parser("ECAC Championships",
        datetime.date(2012,3,11),
        url = request.POST['result_url'])
  return render(request, 'uploads/homepage.html')
