import argparse
from ebook import Ebook

class Blook(object):
  def _sanitize_url(self, url):
    if not url.startswith('http'):
      url = 'https://%s' % url
    if url.endswith('/'):
      url = url.rstrip('/')
    return url

  def run(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to download")
    parser.add_argument(
      "--limit", type=int, default=0, help="Max number of articles to download")
    args = parser.parse_args()
    if not args.url:
      parser.print_help()
      exit(1)

    url = self._sanitize_url(args.url)
    ebook = Ebook(url, args.limit)
    ebook.assemble()
    print("Wrote %s to %s" % (ebook.get_title(), ebook.get_filename()))

if __name__ == '__main__':
  Blook().run()
