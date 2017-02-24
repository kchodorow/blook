import os
import urllib
import urllib2

from urllib2 import URLError

class Cache(object):
    def __init__(self):
        home = os.environ['HOME']
        self.cache_dir = '%s/.cache/blook' % home
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _download(self, url):
        try:
            response = urllib2.urlopen(url)
            html = response.read()
        except URLError, e:
            print(e)
        return html

    def get(self, url):
        filename = "%s/%s" % (self.cache_dir, urllib.quote(url, safe=''))
        if os.path.isfile(filename):
            with open(filename, 'r') as fh:
                html = fh.read()
        else:
            html = self._download(url)
            with open(filename, 'w') as cache_file:
                cache_file.write(html)
        return html
