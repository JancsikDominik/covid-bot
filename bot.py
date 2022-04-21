from bs4 import BeautifulSoup
from lxml import etree
import requests

class CovidScraper:
    def __init__(self):
        self.baseUrl = "https://www.worldometers.info/coronavirus/country/"
        self.response = None
        self.html = None
        self.soup = None
        self.country = None
    
    def getSite(self, country : str):
        self.country = country
        self.response = requests.get(self.baseUrl + self.country)

        if self.response is not None:
            self.html = self.response.text
        else:
            raise Exception("Error getting response")
        
        self.soup = BeautifulSoup(self.html, "html.parser")
        title = self.soup.find('title')

        if "404 Not Found" in title:
            raise Exception("Country not found") 
    
    def getNewsText(self):
        newCases = []
        newsDivs = self.soup.find_all("div", {"class": "news_post"})
        for div in newsDivs:
            text = div.text.strip()
            if not text.isspace():
                newCases.append(text)

        return newCases