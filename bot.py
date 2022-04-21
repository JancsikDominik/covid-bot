from scraper import CovidScraper

scraper = CovidScraper()

scraper.scrapeCountry("hungary")
news = scraper.getNews()

for n in news:
    print(n)
