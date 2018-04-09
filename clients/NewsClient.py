import requests
import json
from random import randrange


class NewsClient(object):
    """ News Client calls the News API."""

    def __init__(self):
        super(NewsClient, self).__init__()
        self.api_key = "a4f2e384aa2646ec85c17fd5ae330639"
        self.hostname = "newsapi.org/v2/top-headlines"
        self.protocol = "https://"

    def get_headlines(self, news_source):
        """Get the Astronomy Photo of the Day!"""
        news_url = self.protocol + self.hostname
        query_strings = {
            "apiKey": self.api_key,
            "sources": news_source
        }
        response = requests.get(news_url, params=query_strings)
        headlines = json.loads(response.text)
        rand_index = randrange(len(headlines['articles']))
        return headlines['articles'][rand_index]
