from bs4 import BeautifulSoup
from cache import Cache
from ebooklib import epub
from wordpress.post import WordpressPost

import utils

class Ebook(object):
  def __init__(self, url):
    self._url = url
    self._assembled = False
    self._cache = Cache()
    self._title = None
    self._filename = None

  def assemble(self):
    page = self._cache.get(self._url)
    soup = BeautifulSoup(page, 'html.parser')
    self._extract_title(soup)
    urls = self._extract_posts(soup)

    book = epub.EpubBook()
    book.set_title(self._title)
    for url in reversed(urls):
      page = self._cache.get(url)
      post = WordpressPost(page)
      book.add_item(post.get_epub_chapter())

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(self._filename, book)
    self._assembled = True;

  def get_title(self):
    assert self._assembled
    return self._title

  def get_filename(self):
    assert self._assembled
    return self._filename

  def _extract_title(self, page):
    self._title = page.title.name
    self._filename = utils.title_to_filename(self._title)

  def _extract_posts(self, page):
    posts = []
    while page:
      posts += self._extract_articles(page)
      page = self._get_next_page(page)
      return posts

  def _extract_articles(self, page):
    post_titles = page.find_all(class_='post-title')
    posts = []
    if not post_titles:
      return posts
    for t in post_titles:
      full_post_link = t.find('a')
      if full_post_link:
        posts.append(t.href)
    return posts

  def _get_next_page(self, page):
    return None
