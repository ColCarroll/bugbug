"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from homepage.views import homepage


class HomePageTest(TestCase):
  """ Team homepages
  """
  def test_root_url_resolves(self):
    """ Tests that home page is found
    """
    found = resolve("/")
    self.assertEqual(found.func, homepage)

  def test_returns_correct_html(self):
    """Makes sure html is formatted correctly
    """
    request = HttpRequest()
    response = homepage(request)
    expected_html = render_to_string('homepage.html')
    self.assertEqual(response.content.decode(), expected_html)

