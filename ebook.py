from bs4 import BeautifulSoup
from cache import PageNotFoundError
from ebooklib import epub
from filters import filter_index
from extract.extractor import Listing, ListingNotFoundError
from extract.post import Entry

import re
import utils

class Ebook(object):
  def __init__(self, url, limit, cache):
    self._url = url
    self._limit = limit
    self._assembled = False
    self._cache = cache
    self._title = None
    self._filename = None

  def assemble(self):
    urls = self._get_urls()
    book = epub.EpubBook()
    spine = [epub.EpubNcx(), epub.EpubNav()]
    toc = []
    for url in reversed(urls):
      cache_entry = self._cache.get(url)
      if not cache_entry:
        continue
      post = Entry(cache_entry, filter_index.ENTRY_FILTERS)
      chapter = post.get_epub_chapter()
      spine.append(chapter)
      toc.append(epub.Link(chapter.file_name, chapter.title, chapter.id))
      for url, filename in post.get_image_urls():
        img = epub.EpubImage()
        img.file_name = filename
        try:
          img.content = self._cache.get(url, binary=True)
          img.media_type = 'image/jpeg'
          book.add_item(img)
        except PageNotFoundError, e:
          # Ignored, just skip the image.
          pass

    book.toc = toc
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

  def _get_urls_under_url(self, url):
    page = self._cache.get(url)
    soup = BeautifulSoup(page, 'html.parser')
    extractor = Listing(page, self._cache)
    urls = extractor.extract(self._limit, filter_index.ENTRY_LISTINGS)
    self._extract_title(soup)
    return urls

  def _get_urls(self):
    original_e = None
    try:
      return self._get_urls_under_url(self._url)
    except (PageNotFoundError, ListingNotFoundError) as e:
      original_e = e

    if re.search('/blog$', self._url):
      raise e

    # Otherwise, retry with /blog appended to the URL.
    try:
      return self._get_urls_under_url('%s/blog' % self._url)
    except e:
      # But don't throw the error with /blog appended, as that would be
      # confusing.
      original_e.write()
      raise original_e

  def _extract_title(self, page):
    self._title = page.title.string.strip()
    self._filename = "%s.epub" % utils.title_to_filename(self._title)
