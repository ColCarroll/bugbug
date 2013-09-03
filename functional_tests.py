""" Functional test suite
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
    self.browser.get('http://localhost:8000')

    #Seeing the page title lets him know he's in the right place
    self.assertIn('BugBug', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('Explore', header_text)

    #He clicks a button to upload new results
    uploadbutton = self.browser.find_element_by_id('upload_button')
    uploadbutton.click()

    #and is taken to the uploads page
    self.assertIn("Uploads", self.browser.title)
    inputbox = self.browser.find_element_by_id("result_url")
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Enter a result url'
        )
    # He enters a url pointing to results and hits enter
    inputbox.send_keys("http://www.coolrunning.com/results/12/ma/Nov3_ECACDi_set1.shtml")
    inputbox.send_keys(Keys.ENTER)

    # This takes him to the parsed results page.
    self.assertIn("Results", self.browser.title)

    self.fail("Finish the test!")

if __name__ == '__main__':
  unittest.main()
