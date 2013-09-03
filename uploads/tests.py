"""
Tests for uploads
"""

import datetime
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from uploads.views import homepage
from uploads.parser import Parser

class ParserTest(TestCase):
  """ Tests parser functionality
  """
  def reads_url(self):
    """ Makes sure parser can read a coolrunniing result
    """
    parser = Parser("ECAC Championships",
        datetime.date(2012,3,11),
        url= \
        "http://www.coolrunning.com/results/12/ma/Nov3_ECACDi_set1.shtml")
    self.assertEqual(287, len(parser.results))
    self.assertIn("Sam Haney", parser.print_results())


class UploadTest(TestCase):
  """ Test upload page
  """
  def test_root_url_resolves(self):
    """ Tests that home page is found
    """
    found = resolve("/uploads/")
    self.assertEqual(found.func, homepage)

  def test_returns_correct_html(self):
    """Makes sure html is formatted correctly
    """
    request = HttpRequest()
    response = homepage(request)
    expected_html = render_to_string('uploads/homepage.html')
    self.assertEqual(response.content.decode(), expected_html)

  def test_save_post(self):
    """ Make sure form can save post requests
    """
    request = HttpRequest()
    request.method = "POST"
    request.POST["result_url"] = \
        "http://www.coolrunning.com/results/12/ma/Nov3_ECACDi_set1.shtml"

    response = homepage(request)

    self.assertIn("Sam Haney", response.content.decode())
