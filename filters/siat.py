from filters.base import BaseEntry, BaseListing, NotFoundError

import re

PREVIOUS_RE = re.compile('Previous ')
OLDER_RE = re.compile('Older ')

class SiatEntry(BaseEntry):
  def applies(self, soup):
    return soup.find(class_='post')

  def extract_title(self, soup):
    post = soup.find(class_='post')
    title_link = post.find('a')
    if not title_link:
      raise NotFoundError('a', post)
    return title_link.get_text()

  def extract_content(self, soup):
    return soup.find(class_='post')

class SiatListing(BaseListing):
  def applies(self, soup):
    return soup.find(class_='post') and soup.find(string=PREVIOUS_RE)

  def extract_urls(self, soup):
    post_titles = soup.find_all(class_='post')
    if not post_titles:
      raise NotFoundError('class="post"', soup)
    urls = []
    for t in post_titles:
      full_post_link = t.find('a', href=True)
      if full_post_link:
        urls.append(full_post_link['href'])
    return urls

  def next_page_url(self, soup):
    prev = soup.find(string=PREVIOUS_RE)
    return prev.parent['href']

class AvcListing(SiatListing):
  """Based on avc.com."""

  def applies(self, soup):
    return soup.find(class_='post') and soup.find(string=OLDER_RE)

  def next_page_url(self, soup):
    prev = soup.find(string=OLDER_RE)
    parent = prev.parent
    while parent and not parent.name == 'a':
      parent = parent.parent
    return parent['href']
