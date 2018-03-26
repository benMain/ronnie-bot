import unittest
import logging
from clients import Nasa


class NasaClientTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('NasaClientTest')

    def test_get_astronomy_photo(self):
        nasa_client = Nasa.NasaClient()
        response = nasa_client.get_astronomy_photo()
        self.assertTrue("url" in response.keys())
        self.assertTrue("explanation" in response.keys())
