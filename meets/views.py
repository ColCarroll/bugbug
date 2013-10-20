""" Meet views
"""
from django.shortcuts import render
from meets.models import Meet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def homepage(request):
  """Home page for teams
  """
  meets = Meet.objects.all().order_by('-date', 'meet_name')
  paginator = Paginator(meets, 50)
  page = request.GET.get('page')
  try:
    meets = paginator.page(page)
  except PageNotAnInteger:
    meets = paginator.page(1)
  except EmptyPage:
    meets = paginator.page(paginator.num_pages)
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
