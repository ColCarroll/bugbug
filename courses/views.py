""" Course views
"""
from django.shortcuts import render
from courses.models import Course

def homepage(request):
  """Home page for courses
  """
  courses = Course.objects.all()
  return render(request,
      'courses/homepage.html',
      {'courses' : courses})

def results(request, course_pk):
  """Home page for a course
  """
  course = Course.objects.get(pk=course_pk)
  courses = Course.objects.filter(host = course.host,
      city = course.city,
      state = course.state)
  return render(request,
      'courses/results.html',
      {'course' : course,
        'courses' : courses,
        })
