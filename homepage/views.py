""" Create your views here.
"""

#from coffin.shortcuts import render_to_response
from django.shortcuts import render

def home_page(request):
  """Home page for teams
  """

  #return render_to_response(request, 'homepage.html')
  return render(request, 'homepage.html')
