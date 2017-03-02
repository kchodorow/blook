from bs4 import BeautifulSoup
from ebooklib import epub
from filters import base

import utils

VERBOTEN_TAGS = [
  'script', 'link', 'meta', 'style', 'media', 'iframe', 'frame', 'video']
VERBOTEN_CLASSES = [
  'postmeta',
  'postmetadata',
  'postnavigation',
  'navigation',
  'wpcnt',  # This seems to be some sort of Wordpress metadata field.
]
VERBOTEN_IDS = [
  'comments',
  'header',
  'footer',
  'sidebar',
  'description',
  'disqus_thread',
  'jp-post-flair',  # More wordpress-isms from lackhand.wordpress.com.
]

class Entry(object):
  """Extracts the actual content of the post and removes all non-ebook
  formatting."""

  def __init__(self, page, filters):
    self._soup = BeautifulSoup(page, 'html.parser')
    self._filters = filters
    self._img_urls = []

    tmpl = None
    for f in self._filters:
      if f.applies(self._soup):
        tmpl = f
        break

    if not tmpl:
      raise EntryFilterNotFoundError(self._soup)

    self._title = tmpl.extract_title(self._soup)
    content = tmpl.extract_content(self._soup)
    self._content = self._scrub_content(content).encode('utf-8')

  def get_epub_chapter(self):
    chapter = epub.EpubHtml(
      uid=utils.generate_uid(self._title),
      title=self._title,
      file_name='%s.xhtml' % utils.title_to_filename(self._title)
    )
    chapter.content = self._content
    return chapter

  def get_image_urls(self):
    return self._img_urls

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

    if content.name == 'img':
      self._add_img(content)
    else:
      imgs = content.find_all('img')
      for img in imgs:
        self._add_img(img)

    return content

  def _add_img(self, img):
    img_src = self._get_img_src(img['src'])
    self._img_urls.append((img['src'], img_src))
    img['src'] = img_src

  def _get_img_src(self, url):
    return url.strip().replace(':', '_c').replace('/', '_s').replace('&', '_a').replace('?', '_q')

class EntryFilterNotFoundError(base.FilterNotFoundError):
  def __init__(self, soup):
    super(EntryFilterNotFoundError, self).__init__(
      'No entry filter found', soup)
