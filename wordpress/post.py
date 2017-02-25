from bs4 import BeautifulSoup
from ebooklib import epub

import utils

class WordpressPost(object):
  def __init__(self, page):
    self._soup = BeautifulSoup(page, 'html.parser')

  def get_epub_chapter(self):
    post = self._soup.find(class_='post')
    if not post:
      post = self._soup.find(class_='post-title')
    if not post:
      # TODO
      return None

    title_link = post.find('a')
    if not title_link:
      print('post: %s' % post.prettify())
      return None

    title_str = title_link.string
    if not title_str:
      print('ln: %s' % title_link.prettify())
      return None

    chapter = epub.EpubHtml(
      title=title_str,
      file_name='%s.xhtml' % utils.title_to_filename(title_str)
    )

    clazz = None
    if self._soup.find('entry-content'):
      clazz = 'entry-content'
    elif self._soup.find('entry'):
      clazz = 'entry'

    title = title_str.encode('utf-8')
    content = self._soup.find(clazz).encode('utf-8')
    chapter.content = '{title_str}{content}'.format(
      title_str=title,
      content=content,
    )
    return chapter
