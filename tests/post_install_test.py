"""
Test Class for Application.
"""
import unittest
from mock import patch
from app import app
import logging
import os


class PostInstallTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.log = logging.getLogger('PostInstallTest')
        os.environ['CLIENT_ID'] = '332778013425.331731360914'
        os.environ['CLIENT_SECRET'] = '270gh503445e430d08aa51b56813d1be'
        os.environ['VERIFICATION_TOKEN'] = 'wubrKYdbYAbMygrmwoIeqnbQ'
        os.environ['BOT_TOKEN'] = 'xoxb-331853501189-jtFkxjOSnoz65LO6ihqCGm2X'

    @patch('slackclient.SlackClient.api_call')
    def test_post_install_page(self, api_auth_mock):
        api_auth_mock.side_effect = [
            {'team_id': 'superTeam', 'bot': {'bot_access_token': 'fakeToken'}}]
        response = self.app.get('/thanks')
        page_data = response.data
        self.assertTrue(isinstance(page_data, str))
        self.assertTrue(
            'Thanks for installing, sucker ... I mean intelligent user.'
            in page_data)
