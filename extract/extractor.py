from bs4 import BeautifulSoup
from filters import base

import logging
import sys

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('extract.extractor.Listing')

class Listing(object):
  """Extracts a list of URLs for individual posts."""

  def __init__(self, page, cache):
    self._page = page
    self._cache = cache

  def extract(self, limit, filters):
    if limit == 0:
      limit = sys.maxint
    listing = None
    page = BeautifulSoup(self._page, 'html.parser')
    for l in filters:
      if l.applies(page):
        listing = l
        logging.debug('Chose listing filter %s', type(listing).__name__)
        break
    if not listing:
      raise ListingNotFoundError(page)

    urls = []
    count = 0
    while page and len(urls) < limit and count < limit:
      urls += listing.extract_urls(page)
      if len(urls) >= limit:
        break
      next_url = listing.next_page_url(page)
      page = None
      if next_url:
        listing_page = self._cache.get(next_url)
        if listing_page:
          page = BeautifulSoup(listing_page, 'html.parser')
      # Safety valve so it doesn't run forever if there's a bug and it can't
      # extract any URLs.
      count = count + 1
    return urls[0:limit]

class ListingNotFoundError(base.FilterNotFoundError):
  def __init__(self, soup):
    super(ListingNotFoundError, self).__init__(
      'No listing filter found', soup)
