from bs4 import BeautifulSoup

import re
import sys

class Extractor(object):
  def __init__(self, page, cache):
    self._page = page
    self._cache = cache
    self._class = None

  def extract(self, limit):
    if limit == 0:
      limit = sys.maxint
    posts = []

    if self._page.find(class_='post-title'):
      # Form is: <h1 class="post-title"><a ...>Title
      self._class = 'post-title'
    elif self._page.find(class_='post'):
      # Form is: <div class="post"><h2><a ...>Title
      self._class = 'post'
    else:
      return posts

    page = self._page
    while page and len(posts) < limit:
      posts += self._extract_articles(page)
      page = self._get_next_page(page)
    return posts[0:limit]

  def _extract_articles(self, page):
    post_titles = page.find_all(class_=self._class)
    posts = []
    if not post_titles:
      return posts
    for t in post_titles:
      full_post_link = t.find('a', href=True)
      if full_post_link:
        posts.append(full_post_link['href'])
    return posts

  def _get_next_page(self, page):
    older = page.find_all(string=re.compile('Older '))
    if not older:
      older = page.find_all(string=re.compile('Previous '))
    if not older:
      return None

    for o in older:
      link = o.parent
      if link.name == 'a' and link['href']:
        page = self._cache.get(link['href'])
        return BeautifulSoup(page, 'html.parser')
