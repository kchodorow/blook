from bs4 import BeautifulSoup

import sys

class Extractor(object):
  """Extracts a list of URLs for individual posts."""

  def __init__(self, page, cache):
    self._page = page
    self._cache = cache
    self._class = None

  def extract(self, limit, filters):
    if limit == 0:
      limit = sys.maxint
    listing = None
    for l in filters:
      if l.applies(self._page):
        listing = l
        break
    if not listing:
      raise ListingNotFoundError(self._page)

    page = self._page
    urls = []
    while page and len(urls) < limit:
      urls += listing.extract_urls(page)
      next_listing = listing.next_page_url(page)
      listing = self._cache.get(next_listing)
      page = None
      if listing:
        page = BeautifulSoup(listing, 'html.parser')
    return urls[0:limit]

class ListingNotFoundError(Exception):
  def __init__(self, soup):
    super(ListingNotFoundError, self).__init__(
      'No filter found for %s' % soup.prettify())
