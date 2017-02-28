from bs4 import BeautifulSoup
from cache import Cache
from ebooklib import epub
from filters.siat import SiatEntry, SiatListing
from filters.veb import VebEntry, VebListing
from wordpress.extractor import Extractor
from wordpress.post import WordpressPost

import utils

ENTRY_FILTERS = [
  SiatEntry(),
  VebEntry(),
]

ENTRY_LISTINGS = [
  SiatListing(),
  VebListing(),
]

class Ebook(object):
  def __init__(self, url, limit):
    self._url = url
    self._limit = limit
    self._assembled = False
    self._cache = Cache()
    self._title = None
    self._filename = None

  def assemble(self):
    page = self._cache.get(self._url)
    soup = BeautifulSoup(page, 'html.parser')
    self._extract_title(soup)
    extractor = Extractor(page, self._cache)
    urls = extractor.extract(self._limit, ENTRY_LISTINGS)

    spine = [epub.EpubNcx(), epub.EpubNav()]
    for url in reversed(urls):
      page = self._cache.get(url)
      post = WordpressPost(page, ENTRY_FILTERS)
      chapter = post.get_epub_chapter()
      if chapter:
        spine.append(chapter)

    book = epub.EpubBook()
    book.set_title(self._title)
    book.spine = spine
    for s in spine:
      book.add_item(s)
    epub.write_epub(self._filename, book)
    self._assembled = True;

  def get_title(self):
    assert self._assembled
    return self._title

  def get_filename(self):
    assert self._assembled
    return self._filename

  def _extract_title(self, page):
    self._title = page.title.string.strip()
    self._filename = "%s.epub" % utils.title_to_filename(self._title)
