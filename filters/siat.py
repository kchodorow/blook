from filters.base import BaseEntry, BaseListing, NotFoundError

import re

class SiatEntry(BaseEntry):
  def applies(self, soup):
    return soup.find(class_='post') and soup.find(class_='entrytext')

  def extract_title(self, soup):
    post = soup.find(class_='post')
    title_link = post.find('a')
    if not title_link:
      raise NotFoundError('a', post)
    return title_link.get_text()

  def extract_content(self, soup):
    return soup.find(class_='post')

PREVIOUS_RE = re.compile('Previous ')

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
