""" Runner views
"""
from django.shortcuts import render
from runners.models import Runner

def results(request, runner_pk):
  """Home page for teams
  """
  runner = Runner.objects.get(pk=runner_pk)
  the_results = runner.result_set.all().order_by('time')
  return render(request,
      'runners/results.html',
      {'runner' : runner,
      'results': the_results})
