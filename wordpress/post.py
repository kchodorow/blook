from bs4 import BeautifulSoup
from ebooklib import epub

import utils

class WordpressPost(object):
  def __init__(self, page):
    self._soup = BeautifulSoup(page, 'html.parser')

  def get_epub_chapter(self):
    title_link = self._soup.find('a')
    title_str = title_link.string
    chapter = epub.EpubHtml(
      title=title_str,
      file_name='%s.xhtml' % utils.title_to_filename(title_str)
    )
    chapter.content = '{title_str}{content}'.format(
      title_str=title_str,
      content=self._soup.find('entry-content').prettify())
    return chapter
