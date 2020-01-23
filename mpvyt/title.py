import hashlib
import os
import requests
from bs4 import BeautifulSoup


CACHE_PATH = os.environ['MPVYT_CACHE_PATH'] \
    if 'MPVYT_CACHE_PATH' in os.environ \
    else os.path.join(os.path.expanduser('~'), '.cache', 'mpvyt')


class TitleLookup:
    """
    Look up titles for playlist items.
    """

    def __init__(self):
        self.cache = {}

    def lookup(self, item):
        title = self.lookup_cache(item)
        if title:
            return title
        if item.startswith('http'):
            return self.lookup_http(item)
        return None

    def get_path(self, item):
        hash = hashlib.sha224(bytes(item, 'utf-8')).hexdigest()
        root, rest = hash[0:2], hash[2:]
        dirs = os.path.join(CACHE_PATH, root)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        return os.path.join(dirs, rest)

    def lookup_cache(self, item):
        if item in self.cache:
            return self.cache[item]
        path = self.get_path(item)
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return f.readline()

    def insert_cache(self, item, title):
        self.cache[item] = title
        with open(self.get_path(item), 'w') as f:
            f.write(title)

    def lookup_http(self, item):
        """
        Simple HTTP lookup based on <title> tag
        """
        r = requests.get(item)
        soup = BeautifulSoup(r.text, features='lxml')
        title = soup.title.string
        self.insert_cache(item, title)
        return title
