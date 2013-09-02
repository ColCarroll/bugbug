"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from teams.views import homepage


class HomePageTest(TestCase):
  """ Team homepages
  """
  def test_root_url_resolves(self):
    """ Tests that team home page is found
    """
    found = resolve("/teams/")
    self.assertEqual(found.func, homepage)

  def test_returns_correct_html(self):
    """Makes sure html is formatted correctly
    """
    request = HttpRequest()
    response = homepage(request)
    self.assertTrue(response.content.startswith(b'<html>'))
    self.assertIn(b'<title>BugBug Teams</title>', response.content)
    self.assertTrue(response.content.endswith(b'</html>'))


