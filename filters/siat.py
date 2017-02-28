from filters.base import BaseEntry, NotFoundError

class Siat(BaseEntry):
  def applies(self, soup):
    return soup.find(class_='post') and soup.find(class_='entrytext')

  def extract_title(self, soup):
    post = soup.find(class_='post')
    title_link = post.find('a')
    if not title_link:
      raise NotFoundError('a', post)
    return title_link.get_text()

  def extract_content(self, soup):
    return soup.find(class_='entrytext')
