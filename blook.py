import argparse
from ebook import Ebook

def _sanitize_url(url):
  if not url.startswith('http'):
    url = 'https://%s' % url
  if url.endswith('/'):
    url = url.rstrip('/')
  return url

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL to download")
args = parser.parse_args()
if not args.url:
  parser.print_help()
  exit(1)

url = _sanitize_url(args.url)

print("url: %s" % url)

ebook = Ebook(url)
ebook.assemble()
print("Wrote %s to %s" % (ebook.get_title(), ebook.get_filename()))
