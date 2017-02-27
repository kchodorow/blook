from bs4 import BeautifulSoup
from cache import Cache
from ebooklib import epub
from wordpress.extractor import Extractor
from wordpress.post import WordpressPost

import utils

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
    urls = self._extract_posts(soup)

    spine = [epub.EpubNcx(), epub.EpubNav()]
    for url in reversed(urls):
      page = self._cache.get(url)
      post = WordpressPost(page)
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

  def _extract_posts(self, page):
    extractor = Extractor(page, self._cache)
    return extractor.extract(self._limit)
