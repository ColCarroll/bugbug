"""Module for scraping results from the internet
"""
import datetime
import re
import requests
from bs4 import BeautifulSoup

from teams.models import Team
from courses.models import Course
from meets.models import Meet
from results.models import Result
from runners.models import Runner

class Scraper:
  """Handles file parsing operations
  """
  def __init__(self,
      url = "http://xc.tfrrs.org/results/xc/5347.html"):

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
    for result_set in self.results:
      for result in result_set:
        result['first_name'], result['last_name'] = (
            j.strip() for j in result.get("Name").split(",")
            )
        time_match = re.match(
            r"(?P<minutes>\d{0,2}):(?P<seconds>\d{2}.?\d{0,2})",
            result['time'])
        result['time'] = (
            60* float(time_match['minutes']) + float(time_match['seconds']))

  def gender_distance(self):
    """ Finds result distances
    """
    distances = self.soup.find_all(
        "a",
        text=re.compile("[Women's|Men's] [0-9]{1,2}k"))
    return [{'gender': re.search(r"(Women|Men)", j.text).group(1),
      'distance': 1000 * int(re.search(r"(\d+)", j.text).group(1))}
      for j in distances]

  def meet_name(self):
    """ Finds the meet name
    """
    return self.soup.find("h2").text.strip()

  def create(self):
    """ Reads results and saves to database
    """
    date_location = self.datelocation()
    gender_distance = self.gender_distance()
    meet_name = self.meet_name()
    self.read_results()
    assert len(self.results) == len(gender_distance)

    for j, result_set in enumerate(self.results):
      course, _ = Course.objects.get_or_create(
          host = date_location.get('host'),
          city = date_location.get('city'),
          state = date_location.get('state'),
          distance = gender_distance[j]['distance'])
      meet, _ = Meet.objects.get_or_create(
          date = date_location.get('date'),
          gender = gender_distance[j]['gender'],
          meet_name = meet_name,
          course = course)
      for result in result_set:
        team, _ = Team.objects.get_or_create(
            name = result('team'))
        runner, _ = Runner.objects.get_or_create(
            first_name = result['first_name'],
            last_name = result['last_name'],
            class_year = result['class_year'],
            )
        runner.teams.add(team)
        result, _ = Result.objects.get_or_create(
            meet = meet,
            runner = runner,
            time = result['time'],
            )



