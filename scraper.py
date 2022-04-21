from inspect import _void
from bs4 import BeautifulSoup
from lxml import etree
import requests


class CovidScraper:
    def __init__(self):
        # initializing members
        self.baseUrl = "https://www.worldometers.info/coronavirus/country/"
        self.response = None
        self.html = None
        self.soup = None
        self.country = None

    def scrapeCountry(self, country: str):
        self.country = country
        self.response = requests.get(self.baseUrl + self.country)

        # if the response failed
        if self.response is not None:
            self.html = self.response.text
        else:
            raise Exception("Error getting response")

        # cooking the soup
        self.soup = BeautifulSoup(self.html, "html.parser")
        title = self.soup.find('title')

        # if we didn't find the page
        if "404 Not Found" in title:
            raise Exception("Country not found")

    # returns an array where each element is a day. day[0] is the new covid cases and day[1] are the new deaths
    # the array goes from newest update to latest update
    def getNews(self) -> list:
        newCases = []
        newsDivs = self.soup.find_all("div", {"class": "news_post"})
        for div in newsDivs:
            text = div.text.strip().replace(',', '')
            if not text.isspace():
                newCases.append([int(s) for s in text.split() if s.isdigit()])

        return newCases
