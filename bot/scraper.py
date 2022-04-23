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
        #getting every div that has an id that starts with newsdate
        dateDivs = self.soup.find_all("div", id=lambda value: value and value.startswith("newsdate"))
        dates = []
        for d in dateDivs:
            #extracting the date from the id (format: newsdate2022-04-23; so we cut the first 8 characters from the string and we are done)
            dates.append(d.attrs["id"][8:])
        
        newsDivs = self.soup.find_all("div", {"class": "news_post"})
        for i in range(0, len(newsDivs)):
            text = newsDivs[i].text.strip().replace(',', '')
            if not text.isspace():
                infectedAndDead = [int(s) for s in text.split() if s.isdigit()]
                #if no new cases were recorded we add a 0
                if(len(infectedAndDead) == 0):
                    infectedAndDead.append(0)
                #if no new deaths were recorded we add a 0
                if(len(infectedAndDead) == 1):
                    infectedAndDead.append(0)
                    
                newCases.append({"numbers": infectedAndDead, "date": dates[i]})

        return newCases
