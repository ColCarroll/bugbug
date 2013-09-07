"""Module for scraping results from the internet
"""
import datetime
import re
import requests
from collections import Counter
from bs4 import BeautifulSoup

ALLOWED_EXTENSIONS = set(["txt"])
def allowed_file(filename):
  """Makes sure file is in the allowed list
  """
  return (("." in filename) and
      (filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS))

def find_all(regex, string):
  """Returns index of all substrings matching the
  given regex
  """
  return [m.start() for m in re.finditer(regex, string)]

class NumParser:
  """Helper class to parse time and place fields
  """
  def __init__(self):
    self.time_pattern = re.compile(
        r"([0-9]{1,2})?(?::)([0-9]{1,2})(.[0-9]{1,2})?")
    self.place_pattern = re.compile(
        r"^(\d+)(?:\.)?(?<=$)")

  def has_time(self, string):
    """Checks whether the given string has a timestamp in it
    """
    return any(self.time_pattern.match(field) for
        field in string.split())

  def return_time(self, string):
    """Returns largest timestamp from the string
    """
    timestamp = datetime.timedelta(seconds = 0)
    for _, field in self.get_timefields(string):
      group = field.groups()
      times = {
          "minutes": int(group[0] or 0),
          "seconds": int(group[1]) + float(group[2] or 0)}
      newtime = datetime.timedelta(**times)
      if newtime > timestamp:
        timestamp = newtime
    return timestamp

  def get_timefields(self, string):
    """Returns a tuple (index, field) of any time fields
    in the string.  field is a regex match object
    """
    for j, field in enumerate(string.split()):
      match = self.time_pattern.search(field)
      if match:
        yield (j, match)

  def split_on_times(self, string):
    """Splits a string on time fields.  Returns a list of strings
    """
    return re.split("|".join([field[1].string for
      field in self.get_timefields(string)]), string)

  def has_place(self, string):
    """Checks whether the given string has a (possible)
    place at the start
    """
    return any(self.place_pattern.match(field) for
        field in string.split())

  def return_place(self, string):
    """Returns a digit at the start of a line
    """
    for field in string.split():
      field = self.place_pattern.match(field)
      if field:
        return int(field.group(1))

class Scraper:
  """Handles file parsing operations
  """
  def __init__(self,
      url = "http://xc.tfrrs.org/results/xc/5347.html"):

    self.num_parser = NumParser()
    self.data = requests.get(url).text
    self.soup = BeautifulSoup(self.data)
    self.results = []

  def datelocation(self):
    """Parses date and location
    """
    date_location = self.soup.find('ul', class_='datelocation').text
    datestring = re.search(r"Date: ([\d]{2}/[\d]{2}/[\d]{2})", date_location)
    if datestring:
      date = datetime.datetime.strptime(datestring.group(1), "%m/%d/%y").date()
    locstring = re.search(r"Location: (.*)", date_location)
    if locstring:
      locstring = locstring.group(1).split("-")
      host = locstring[0].strip()
      city = locstring[1].split(",")[0].strip()
      state = locstring[1].split(",")[1].strip()
    return {
        "date": date,
        "host": host,
        "city": city,
        "state": state,
        }

  def read_results(self):
    """ Parses result tables
    """
    for table in self.soup.find_all("table"):
      headers = table.find_all(class_="tableHeader")
      if headers and headers[0].text.strip() == "Place":
        self.results.append([])
        theaders = [j.text.strip() for j in headers]
        rows = table.find_all("tr")
        for row in rows:
          cols = row.find_all("td", class_="tableText")
          if cols and len(cols) == len(theaders):
            self.results[-1].append({theaders[j]: cols[j].text.strip()
                for j in range(len(cols))})

  def gender_distance(self):
    """ Finds result distances
    """
    distances = self.soup.find_all(
        "a",
        text=re.compile("[Women's|Men's] [0-9]{1,2}k"))
    return [{'gender': re.search(r"(Women|Men)", j.text).group(1),
      'distance': 1000 * int(re.search(r"(\d+)", j.text).group(1))} for j in distances]

