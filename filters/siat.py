from filters.base import BaseEntry, BaseListing, NotFoundError

import re

PREVIOUS_RE = re.compile('Previous ')
OLDER_RE = re.compile('Older ')
CONTINUE_RE = re.compile('continue reading')
NEXT_RE = re.compile('Next ')

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

class PostListing(BaseListing):
  def applies(self, soup):
    return soup.find(class_='post')

  def extract_urls(self, soup):
    post_titles = soup.find_all(class_='post')
    return self._extract_urls_helper(post_titles)

  def _extract_urls_helper(self, post_titles):
    urls = []
    for t in post_titles:
      full_post_link = t.find('a', href=True)
      if full_post_link:
        urls.append(full_post_link['href'])
    return urls

class SiatListing(PostListing):
  def applies(self, soup):
    return PostListing.applies(self, soup) and soup.find(string=PREVIOUS_RE)

  def next_page_url(self, soup):
    prev = soup.find(string=PREVIOUS_RE)
    while prev.parent and not prev.parent.name == 'a':
      prev = prev.parent
    if not prev.parent:
      raise NotFoundException('a', soup)
    return prev.parent['href']

class AvcListing(PostListing):
  """Based on avc.com."""

  def applies(self, soup):
    return soup.find('h2', class_='post-title') and soup.find(string=OLDER_RE)

  def extract_urls(self, soup):
    post_titles = soup.find_all('h2', class_='post-title')
    return PostListing._extract_urls_helper(self, post_titles)

  def next_page_url(self, soup):
    prev = soup.find(string=OLDER_RE)
    if not prev:
      return None
    parent = prev.parent
    while parent and not parent.name == 'a':
      parent = parent.parent
    return parent['href']

class MmmListing(SiatListing):
  """Based on Mr. Money Moustache."""

  def applies(self, soup):
    return soup.find('article') and soup.find(string=PREVIOUS_RE)

  def extract_urls(self, soup):
    articles = soup.find_all('article')
    urls = []
    for t in articles:
      continue_reading = t.find(string=CONTINUE_RE)
      if not continue_reading:
        continue
      urls.append(continue_reading.parent['href'])
    return urls

class MmmEntry(BaseEntry):
  """Based on Mr. Money Moustache."""

  def applies(self, soup):
    return soup.find(class_='headline') and soup.find(class_='post_content')

  def extract_title(self, soup):
    return soup.find(class_='headline').get_text()

  def extract_content(self, soup):
    return soup.find(class_='post_content')

class NhlListing(BaseListing):
  def applies(self, soup):
    return soup.find('article') and soup.find(string=NEXT_RE)

  def extract_urls(self, soup):
    articles = soup.find_all('article')
    urls = []
    for a in articles:
      heading = a.find('h2')
      if not heading:
        continue
      link = heading.find('a')
      if not link:
        continue
      urls.append(link['href'])
    return urls

  def next_page_url(self, soup):
    prev = soup.find(string=NEXT_RE)
    return prev.parent['href']

class LackhandListing(AvcListing):
  def applies(self, soup):
    return PostListing.applies(self, soup) and \
      soup.find('h2', class_='entry-title') and soup.find(string=OLDER_RE)

  def extract_urls(self, soup):
    post_titles = soup.find_all('h2', class_='entry-title')
    return PostListing._extract_urls_helper(self, post_titles)

class LackhandEntry(BaseEntry):
  def applies(self, soup):
    return soup.find(id='content') and soup.find(class_='entry-title')

  def extract_title(self, soup):
    return soup.find(class_='entry-title').get_text()

  def extract_content(self, soup):
    return soup.find(class_='entry')
