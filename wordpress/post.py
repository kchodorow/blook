from bs4 import BeautifulSoup
from ebooklib import epub

import utils

VERBOTEN_TAGS = [
  'script', 'link', 'meta', 'style', 'media', 'iframe', 'frame', 'video']
VERBOTEN_CLASSES = ['postmetadata', 'navigation']
VERBOTEN_IDS = [
  'comments', 'header', 'footer', 'sidebar', 'description', 'disqus_thread']

class WordpressPost(object):
  """Extracts the actual content of the post and removes all non-ebook
  formatting."""

  def __init__(self, page, filters):
    self._soup = BeautifulSoup(page, 'html.parser')
    self._filters = filters

  def get_epub_chapter(self):
    tmpl = None
    for f in self._filters:
      if f.applies(self._soup):
        tmpl = f
        break

    if not tmpl:
      raise EntryFilterNotFoundError(self._soup)

    title = tmpl.extract_title(self._soup)
    content = tmpl.extract_content(self._soup)

    chapter = epub.EpubHtml(
      uid=utils.generate_uid(title),
      title=title,
      file_name='%s.xhtml' % utils.title_to_filename(title)
    )

    content = self._scrub_content(content).encode('utf-8')
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

class EntryFilterNotFoundError(Exception):
  def __init__(self, soup):
    super(EntryFilterNotFoundError, self).__init__(
      'No filter found for %s' % soup.prettify())
