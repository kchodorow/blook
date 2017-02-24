import argparse
from cache import Cache

#from bs4 import BeautifulSoup

def _sanitize_url(url):
    if not url.startswith('http'):
        url = 'https://%s' % url
    if url.endswith('/'):
        url = url.rstrip('/')
    return url

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to download")
args = parser.parse_args()
url = _sanitize_url(args.url)

print("url: %s" % url)
cache = Cache()
html = cache.get(url)
print(html)

#soup = BeautifulSoup(html, 'html.parser')
