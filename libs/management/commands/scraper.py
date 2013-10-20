"""Module for scraping results from the internet
"""
import sys
import traceback
import datetime
import re
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from teams.models import Team
from courses.models import Course
from meets.models import Meet
from results.models import Result, Url
from runners.models import Runner


def get_links():
  """Scrapes results links
  """
  more_data = True
  page = 0
  page_url = "http://www.tfrrs.org/results_search.html?page={0}&sport=xc&title=1&go=1"
  links = []

  while more_data:
    old_len = len(links)
    more_data = False
    url = page_url.format(page)
    data = requests.get(url).text
    soup = BeautifulSoup(data)
    page_links = soup.find_all("td", class_="meet")
    for link in page_links:
      if link.find("a"):
        if len(links) > old_len + 1:
          more_data = True
        links.append(link.find("a")["href"])
    if more_data:
      page += 1
    print("{0} links found".format(len(links)))
  new_links = [link for link in links if not Url.objects.filter(url=link).exists()]
  print("{:d} new links found".format(len(new_links)))
  return new_links


class Scraper:
  """Handles file parsing operations
"""

  def __init__(self,
               url="http://www.tfrrs.org/results/xc/5403.html"):
    self.url = url
    self.data = requests.get(url).text
    self.soup = BeautifulSoup(self.data)
    self.results = []

  def datelocation(self):
    """Parses date and location
  """
    date_location = self.soup.find('ul', class_='datelocation').text
    datestring = re.search(r"Date: ([\d]{2}/[\d]{2}/[\d]{2})",
                           date_location)
    if datestring:
      date = datetime.datetime.strptime(datestring.group(1),
                                        "%m/%d/%y").date()
    locstring = re.search(r"Location: (.*)", date_location)
    if locstring:
      locstring = locstring.group(1).split("-")
      host = "-".join(locstring[:-1]).strip()
      city = locstring[-1].split(",")[0].strip()
      state = locstring[-1].split(",")[1].strip()
    return {
      "date": date,
      "host": host,
      "city": city,
      "state": state,
    }

  def read_results(self):
    """ Parses result tables
  """
    result_year = {'FR-1': 4,
                   "SO-2": 3,
                   "JR-3": 2,
                   "SR-4": 1,
                   "FR": 4,
                   "SO": 3,
                   "JR": 2,
                   "SR": 1,
                   "Freshman": 4,
                   "Sophomore": 3,
                   "Junior": 2,
                   "Senior": 1,
                   "": 1, }
    year = int(self.datelocation()['date'].year)
    for table in self.soup.find_all("table"):
      headers = table.find_all(class_="tableHeader")
      if headers and headers[0].text.strip() == "Place":
        self.results.append([])
        theaders = [j.text.strip() for j in headers]
        rows = table.find_all("tr")
        for row in rows:
          cols = row.find_all("td", class_="tableText")
          if cols and len(cols) == len(theaders):
            self.results[-1].append(
              {
                theaders[j]: cols[j].text.strip()
                for j in range(len(cols))})
    for result_set in self.results:
      for result in result_set:
        try:
          result['last_name'], result['first_name'] = ( \
            j.strip() for j in result.get("Name").split(",")
          )
        except ValueError:
          names = [j.strip() for j in result.get("Name").split(",")]
          result['last_name'] = "'".join(names[:-1])
          result['first_name'] = names[-1]
        if len(re.findall(r"[:]", result["Time"])) == 1:
          time_match = re.match(
            r"(?P<minutes>\d{0,2}):(?P<seconds>\d{2}.?\d{0,2})",
            result['Time'])
          result['Time'] = (
            60 * float(time_match.group('minutes')) +
            float(time_match.group('seconds')))
        else:
          time_match = re.match(
            r"(?P<hours>\d{0,2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}.?\d{0,2})",
            result['Time'])
          result['Time'] = (
            3600 * float(time_match.group('hours')) +
            60 * float(time_match.group('minutes')) +
            float(time_match.group('seconds')))
        result['class_year'] = result_year.get(result['Year'], 1) + year

  def gender_distance(self):
    """ Finds result distances
  """
    gender_distances = []
    distances = self.soup.find_all(
        "div",
        style="margin-left: 10px; color: #000; font-weight: bold;")

    for j in distances:
      if re.search(r"(Men|Male)", j.text):
        gender = "Men"
      elif re.search(r"(Women|Female)", j.text):
        gender = "Women"
      else:
        gender = "Null"
      units = re.search(r"\((\d+)", j.text)
      if not units:
        units = 0
      else:
        units = int(units.group(1))
      if units <= 1:
        units = 0
      if "mi" in j.text.lower():
        distance = 1609 * units
      elif "k" in j.text.lower():
        distance = 1000 * units
      else:
        distance = 0
      gender_distances.append({"distance": distance, "gender": gender})
    return gender_distances

  def meet_name(self):
    """ Finds the meet name
    """
    return self.soup.find("h2").text.strip()

  def create(self):
    """ Reads results and saves to database
    """
    date_location = self.datelocation()
    gender_distances = self.gender_distance()
    this_meet_name = self.meet_name()
    self.read_results()
    assert len(self.results) == len(gender_distances), \
      "results have length {0}, found  {1} distances".format(
        len(self.results),
        len(gender_distances))

    for j, result_set in enumerate(self.results):
      course, _ = Course.objects.get_or_create(
        host=date_location.get('host'),
        city=date_location.get('city'),
        state=date_location.get('state'),
        distance=gender_distances[j]['distance'])
      meet, _ = Meet.objects.get_or_create(
        date=date_location.get('date'),
        gender=gender_distances[j]['gender'],
        meet_name=this_meet_name,
        course=course)
      for result in result_set:
        team, _ = Team.objects.get_or_create(
          name=result['Team'])
        runner, _ = Runner.objects.get_or_create(
          first_name=result['first_name'],
          last_name=result['last_name'],
          class_year=result['class_year'],
          team=team,
        )
        result, _ = Result.objects.get_or_create(
          meet=meet,
          runner=runner,
          time=result['Time'],
        )

  def success(self):
    """
    Used to mark that reading the url was a success
    """
    Url.objects.create(url=self.url)


class Command(BaseCommand):
  help = "Scrapes results from web"

  def handle(self, *args, **options):
    links = get_links()
    for link in links:
      print("Scraping {0}".format(link))
      scraper = Scraper(link)
      try:
        scraper.create()
        scraper.success()
      except BaseException as e:
        traceback.print_exception(*sys.exc_info(), limit=2)
