import unittest
import logging
import json
from clients import Nasa


class NasaClientTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('NasaClientTest')

    def test_get_astronomy_photo(self):
        nasa_client = Nasa.NasaClient()
        response = nasa_client.get_astronomy_photo()
        response_dict = json.loads(response.text)
        print(response_dict)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("url" in response_dict.keys())
        self.assertTrue("explanation" in response_dict.keys())
