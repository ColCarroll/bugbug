""" Meet views
"""
from django.shortcuts import render
from meets.models import Meet

def homepage(request):
  """Home page for teams
  """
  meets = Meet.objects.all()
  return render(request,
      'meets/homepage.html',
      {'meets' : meets})

def results(request, meet_pk):
  """Home page for teams
  """
  meet = Meet.objects.get(pk=meet_pk)
  the_results = meet.result_set.all().order_by('time')
  return render(request,
      'meets/results.html',
      {'meet' : meet,
      'results': the_results})
