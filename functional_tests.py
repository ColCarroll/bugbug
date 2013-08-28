""" Functional test suite
"""
import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
  """ Tells story of a new visitor to the site
  """

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_upload_and_view_result(self):
    """Navigate to uploads, enter results
    """
    # Mitchell visits the homepage of a results app
    self.browser.get('http://localhost:5000')

    #Seeing the page title lets him know he's in the right place
    self.assertIn('BugBug', self.browser.title)
    self.fail("Finish the test!")

    #He clicks a button to upload new results and is taken to the uploads
    #page.  He enters a url pointing to results, and clicks the upload
    #button.  After a series of confirmation screens, this takes him to
    #the parsed results page.

if __name__ == '__main__':
  unittest.main()
