import requests
from bs4 import BeautifulSoup


class News:
    headlines = []
    descriptions = []
    newsType = 0
    def __init__(self):
        self.url = ["http://feeds.bbci.co.uk/news/rss.xml", "http://feeds.bbci.co.uk/news/world/rss.xml",
               "http://feeds.bbci.co.uk/news/uk/rss.xml", "http://feeds.bbci.co.uk/news/business/rss.xml",
               "http://feeds.bbci.co.uk/news/politics/rss.xml", "http://feeds.bbci.co.uk/news/health/rss.xml",
               "http://feeds.bbci.co.uk/news/education/rss.xml",
               "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
               "http://feeds.bbci.co.uk/news/technology/rss.xml",
               "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"]

    def getNews(self):
        resp = requests.get(self.url[self.newsType])
        soup = BeautifulSoup(resp.content, features="xml")
        soup.prettify()
        soup.find_all(["a", "b"])
        item = soup.findAll('item')
        newsHeadlines = []
        newsDescriptions = []
        for items in item:
            newsHeadlines.append(items.title.text)
            newsDescriptions.append(items.description.text)
        return newsHeadlines, newsDescriptions

    def printNewsheadlines(self):
        newsHeadlines, newsDescriptions = self.getNews()
        for i in range(len(newsHeadlines)):
            print(newsHeadlines[i])

    def setNewsType(self, newType):
        self.newsType = newType

    def updateAttributes(self):
        print("Updating news headlines")
        self.headlines, self.descriptions = self.getNews()
