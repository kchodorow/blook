from filters.base import BaseEntry, BaseListing, NotFoundError

import re

class SsssEntry(BaseEntry):
  def applies(self, soup):
    return soup.find(class_='pagenum') and soup.find(class_='comicnormal')

  def extract_title(self, soup):
    pp = soup.find(class_='pagenum')
    return pp.get_text()

  def extract_content(self, soup):
    return soup.find(class_='comicnormal')

class SsssListing(BaseListing):
  def applies(self, soup):
    return soup.find(id='navprev')

  def extract_urls(self, soup):
    return [soup.find(id='navprev').parent['href']]

  def next_page_url(self, soup):
    return soup.find(id='navprev').parent['href']
