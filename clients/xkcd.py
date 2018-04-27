import requests
import json
from random import randrange


class XKCDClient(object):
    """ XKCDClient """

    def __init__(self):
        super(XKCDClient, self).__init__()
        self.hostname = "xkcd.com"
        self.protocol = "https://"

    def get_comic(self):
        """Get the XKCD comic!"""
        rand_index = randrange(1980)
        xkcd_url = self.protocol + self.hostname
        xkcd_url += "/{0!s}/info.0.json".format(rand_index)
        response = requests.get(xkcd_url)
        comic = json.loads(response.text)
        return comic
