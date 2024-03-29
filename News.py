import requests
from bs4 import BeautifulSoup


class News:
    def __init__(self):
        self.url = ["http://feeds.bbci.co.uk/news/rss.xml", "http://feeds.bbci.co.uk/news/world/rss.xml",
               "http://feeds.bbci.co.uk/news/uk/rss.xml", "http://feeds.bbci.co.uk/news/business/rss.xml",
               "http://feeds.bbci.co.uk/news/politics/rss.xml", "http://feeds.bbci.co.uk/news/health/rss.xml",
               "http://feeds.bbci.co.uk/news/education/rss.xml",
               "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
               "http://feeds.bbci.co.uk/news/technology/rss.xml",
               "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"]
        self.headlines = ["Headline"]
        self.descriptions = ["Description"]
        self.newsType = 0

    def getNews(self):
        resp = []
        while True:
            try:
                resp = requests.get(self.url[self.newsType])
                break
            except: #requests.exceptions.Timeout:
                print("News connection error")
                time.sleep(5)
                pass
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
        self.headlines, self.descriptions = self.getNews()
