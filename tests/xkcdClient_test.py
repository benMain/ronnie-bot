import unittest
import logging
from clients import xkcd


class XkcdClientTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('XkcdClientTest')

    def test_get_headlines(self):
        xkcd_client = xkcd.XKCDClient()
        response = xkcd_client.get_comic()
        self.assertTrue("title" in response.keys())
        self.assertTrue("transcript" in response.keys())
        self.assertTrue("img" in response.keys())
        self.log.info(response["title"])
        self.log.info(response["img"])
