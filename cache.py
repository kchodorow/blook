import glob
import os
import re
import sys
import time
import urllib
import urllib2

from urllib2 import URLError

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

class Cache(object):
    def __init__(self, url):
      home = os.environ['HOME']
      self._base_url = url
      self._cache_dir = '%s/.cache/blook' % home
      if not os.path.isdir(self._cache_dir):
        os.makedirs(self._cache_dir)
      self._last_download = 0

    def clean(self):
      filename = "%s/%s" % (self._cache_dir, urllib.quote(self._base_url, safe=''))
      for file in glob.glob('%s*' % filename):
        print('Deleting %s' % file)
        os.remove(file)

    def _download(self, url):
      current_time = time.time()
      if current_time - self._last_download < 1:
        # Don't hammer a server
        time.sleep(1)
      self._last_download = current_time

      try:
        sys.stdout.write('Downloading %s...' % url)
        request = urllib2.Request(url)
        request.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(request)
        html = response.read()
      except urllib2.HTTPError, e:
        print(e.reason)
        raise e
      sys.stdout.write(u'\u2714\n')
      return html

    # Visible for testing.
    def get_full_url(self, partial_url):
      if re.match('^https?://', partial_url):
        # Absolute URL.
        return partial_url
      elif partial_url.startswith('/'):
        # Full URI.
        first_slash = self._base_url.find(
          '/', self._base_url.find('://') + len('://'))
        if first_slash == -1:
          first_slash = len(self._base_url)
        return '%s%s' % (self._base_url[0:first_slash], partial_url)
      elif partial_url.startswith('?'):
        qmark_index = self._base_url.rfind('?')
        if qmark_index == -1:
          return '%s%s' % (self._base_url, partial_url)
        return '%s%s' % (self._base_url[0:qmark_index], partial_url)
      else:
        # Relative to wherever we are.
        last_slash = self._base_url.rfind('/')
        if last_slash <= len('https://'):
          last_slash = len(self._base_url)
        return "%s/%s" % (self._base_url[0:last_slash], partial_url)

    def get(self, partial_url, binary=False):
      url = self.get_full_url(partial_url)
      filename = "%s/%s" % (self._cache_dir, urllib.quote(url, safe=''))
      if os.path.isfile(filename):
        mode = 'rb' if binary else 'r'
        with open(filename, mode) as fh:
          html = fh.read()
      else:
        html = self._download(url)
        with open(filename, 'w') as cache_file:
          mode = 'wb' if binary else 'w'
          cache_file.write(html)
      return html
