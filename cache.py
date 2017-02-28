import os
import urllib
import urllib2

from urllib2 import URLError

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

class Cache(object):
    def __init__(self):
        home = os.environ['HOME']
        self.cache_dir = '%s/.cache/blook' % home
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _download(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', USER_AGENT)
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, e:
            print(e.reason)
            raise e
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
