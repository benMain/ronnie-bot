import requests
import datetime
import json
from random import randrange


class NasaClient(object):
    """NasaClient connects to Nasa's APIs."""

    def __init__(self):
        super(NasaClient, self).__init__()
        self.api_key = "lv6BIpM5UvFd52rXHPweBLkq5BJSId2R1nkmRpR8"
        self.hostname = "api.nasa.gov"
        self.protocol = "https://"

    def get_astronomy_photo(self):
        """Get the Astronomy Photo of the Day!"""
        photo_url = self.protocol + self.hostname + "/planetary/apod"
        random_datetime = random_date(datetime.datetime(
            2010, 1, 1), datetime.datetime.now())
        query_strings = {
            "api_key": self.api_key,
            "hd": "true",
            "date": random_datetime.date().isoformat()
        }
        response = requests.get(photo_url, params=query_strings)
        return json.loads(response.text)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)
