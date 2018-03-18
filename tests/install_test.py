"""
Test Class for Application.
"""
import unittest
from app import app
import logging
import os


class InstallTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.log = logging.getLogger('InstallTest')
        os.environ['CLIENT_ID'] = '332778013425.331731360914'
        os.environ['CLIENT_SECRET'] = '270gh503445e430d08aa51b56813d1be'
        os.environ['VERIFICATION_TOKEN'] = 'wubrKYdbYAbMygrmwoIeqnbQ'
        os.environ['BOT_TOKEN'] = 'xoxb-331853501189-jtFkxjOSnoz65LO6ihqCGm2X'

    def test_install_page(self):
        response = self.app.get('/install')
        page_data = response.data
        self.assertTrue(isinstance(page_data, str))
        self.assertTrue('Install ronnie-bot or Else!!!' in page_data)
