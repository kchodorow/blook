from bs4 import BeautifulSoup
from ebooklib import epub

import utils

VERBOTEN_TAGS = [
  'script', 'link', 'meta', 'style', 'media', 'iframe', 'frame', 'video']
VERBOTEN_CLASSES = ['postmetadata', 'navigation']
VERBOTEN_IDS = [
  'comments', 'header', 'footer', 'sidebar', 'description', 'disqus_thread']

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
    content = self._scrub_content(self._soup.find(clazz)).encode('utf-8')
    chapter.content = content
    return chapter

  def _scrub_content(self, content):
    tags_to_remove = []
    for d in content.descendants:
      if d.name in VERBOTEN_TAGS:
        tags_to_remove.append(d)
    for c in VERBOTEN_CLASSES:
      tags_to_remove += content.find_all(class_=c)
    for i in VERBOTEN_IDS:
      tags_to_remove += content.find_all(id=i)

    for d in tags_to_remove:
      d.decompose()

    return content
