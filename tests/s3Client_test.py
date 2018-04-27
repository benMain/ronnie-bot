import unittest
import logging
from datetime import datetime
from clients import s3


class S3ClientTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('S3ClientTest')

    def test_get_headlines(self):
        s3_client = s3.S3Client()
        current_datetime = datetime.utcnow()
        s3_client.write_last_post(current_datetime)
        response_datetime = s3_client.get_last_post()
        self.assertEqual(current_datetime.hour, response_datetime.hour)
        self.assertEqual(current_datetime.minute, response_datetime.minute)
        self.assertEqual(current_datetime.second, response_datetime.second)
