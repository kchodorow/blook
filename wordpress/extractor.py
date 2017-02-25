class Extractor(object):
  def __init__(self, page):
    self._page = page
    self._class = None

  def extract(self):
    posts = []

    if self._page.find(class_='post-title'):
      # Form is: <h1 class="post-title"><a ...>Title
      self._class = 'post-title'
    elif self._page.find(class_='post'):
      # Form is: <div class="post"><h2><a ...>Title
      self._class = 'post'
    else:
      return posts

    page = self._page
    while page:
      posts += self._extract_articles(page)
      page = self._get_next_page(page)
    return posts

  def _extract_articles(self, page):
    post_titles = page.find_all(class_=self._class)
    posts = []
    if not post_titles:
      return posts
    for t in post_titles:
      full_post_link = t.find('a', href=True)
      if full_post_link:
        print("adding %s" % full_post_link['href'])
        posts.append(full_post_link['href'])
    return posts

  def _get_next_page(self, page):
    return None
