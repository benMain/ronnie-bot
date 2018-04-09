import unittest
import logging
from clients import NewsClient


class NewsClientTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('NewsClientTest')

    def test_get_headlines(self):
        news_client = NewsClient.NewsClient()
        response = news_client.get_headlines("techcrunch")
        self.assertTrue("title" in response.keys())
        self.assertTrue("description" in response.keys())
        self.assertTrue("urlToImage" in response.keys())
