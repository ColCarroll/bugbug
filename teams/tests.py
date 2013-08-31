"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import resolve
from django.test import TestCase
from teams.views import home_page


class HomePageTest(TestCase):
  """ Team homepages
  """
  def test_root_url_resolves_to_home_page_view(self):
    """
    Tests that 1 + 1 always equals 2.
    """
    found = resolve("/")
    self.assertEqual(found.func, home_page)
