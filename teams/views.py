""" Team views
"""
from django.shortcuts import render
from teams.models import Team
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def homepage(request):
  """Home page for teams
  """
  teams = Team.objects.all()\
      .annotate(runners =Count('runner'))\
      .order_by('-runners')
  paginator = Paginator(teams, 50)
  page = request.GET.get('page')
  try:
    teams = paginator.page(page)
  except PageNotAnInteger:
    teams = paginator.page(1)
  except EmptyPage:
    teams = paginator.page(paginator.num_pages)
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
