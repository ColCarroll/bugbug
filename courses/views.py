""" Course views
"""
from django.shortcuts import render
from django.db.models import Count
from courses.models import Course
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def homepage(request):
  """Home page for courses
  """
  courses = Course.objects.all().annotate(n_meets=Count('meet')).order_by('-n_meets')
  paginator = Paginator(courses, 50)
  page = request.GET.get('page')
  try:
    courses = paginator.page(page)
  except PageNotAnInteger:
    courses = paginator.page(1)
  except EmptyPage:
    courses = paginator.page(paginator.num_pages)
  return render(request,
                'courses/homepage.html',
                {'courses': courses})


def results(request, course_pk):
  """Home page for a course
  """
  course = Course.objects.get(pk=course_pk)
  courses = Course.objects.filter(host=course.host,
                                  city=course.city,
                                  state=course.state)
  return render(request,
                'courses/results.html',
                {'course': course,
                 'courses': courses,
                })
