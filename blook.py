import argparse
from cache import Cache
from ebook import Ebook
from filters import base

class Blook(object):
  def _sanitize_url(self, url):
    if not url.startswith('http'):
      url = 'https://%s' % url
    if url.endswith('/'):
      url = url.rstrip('/')
    return url

  def run(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to download")
    parser.add_argument(
      "--limit", type=int, default=0, help="Max number of articles to download")
    parser.add_argument('--clean_cache', action='store_true')
    args = parser.parse_args()
    if not args.url:
      parser.print_help()
      exit(1)

    url = self._sanitize_url(args.url)

    if args.clean_cache:
      Cache(url).clean()
      return

    ebook = Ebook(url, args.limit)
    try:
      ebook.assemble()
    except base.FilterNotFoundError, e:
      print("""
ERROR: Blook could not figure out how to parse {url}.

To add support for downloading this blog, please create an issue at
https://github.com/kchodorow/blook/issues with the following title:

    {msg} for {url}

Blook created a file called 'unparsable.html' in this directory, which contains
the HTML it didn't recognize. Please attach it to the GitHub issue.
""".format(url=url, msg=e.message))
      return

    print("Wrote %s to %s" % (ebook.get_title(), ebook.get_filename()))

if __name__ == '__main__':
  Blook().run()
