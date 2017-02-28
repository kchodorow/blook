from filters.base import BaseEntry, BaseListing, NotFoundError

import re

class VebEntry(BaseEntry):
  def applies(self, soup):
    return soup.find(class_='post-title') and soup.find(class_='entry-content')

  def extract_title(self, soup):
    post = soup.find(class_='post-title')
    title_link = post.find('a')
    if not title_link:
      raise NotFoundError('a', post)
    return title_link.get_text()

  def extract_content(self, soup):
    return soup.find(class_='entry-content')

class VebListing(BaseListing):
  def applies(self, soup):
    return soup.find(class_='post-title')

  def extract_urls(self, soup):
    post_titles = soup.find_all(class_='post-title')
    if not post_titles:
      raise NotFoundError('class="post-title"', soup)
    urls = []
    for t in post_titles:
      full_post_link = t.find('a', href=True)
      if full_post_link:
        urls.append(full_post_link['href'])
    return urls

  def next_page_url(self, soup):
    nav = soup.find(class_='pagenav')
    if not nav:
      return None
    current_page = nav.find(class_='current')
    if not current_page or not current_page.next_sibling:
      return None
    return current_page.next_sibling['href']
