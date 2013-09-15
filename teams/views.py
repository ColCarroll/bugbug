""" Team views
"""
from django.shortcuts import render
from teams.models import Team

def homepage(request):
  """Home page for teams
  """
  teams = Team.objects.all()
  teams = sorted(teams,
      key = lambda j:j.runner_set.count(), reverse = True)
  return render(request,
      'teams/homepage.html',
      {'teams' : teams})

def roster(request, team_pk):
  """ Displays information on a single team
  """
  team = Team.objects.get(pk = team_pk)
  runners = team.runner_set.all()
  runners = sorted(runners,
      key = lambda j:(j.result_set.count(), j.class_year), reverse = True)
  men = (j for j in runners if j.gender == "Men")
  women = (j for j in runners if j.gender == "Women")
  return render(request,
      'teams/roster.html',
      {'team': team,
        'men' : men,
        'women': women})
