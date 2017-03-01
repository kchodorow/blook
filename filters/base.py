class BaseEntry(object):
  """Extracts a post's title/content."""

  def applies(self, soup):
    """Returns if this filter recognizes the given soup."""
    return False

  def extract_title(self, soup):
    """Returns the title of this soup."""
    raise NotImplementedError

  def extract_content(self, soup):
    """Returns the content of this soup."""
    raise NotImplementedError

class BaseListing(object):
  """Extracts lists of URLs from index/archive pages."""

  def applies(self, soup):
    """Returns if this filter recognizes the given soup."""
    return False
  def extract_urls(self, soup):
    """Returns urls for posts listed in this soup."""
    raise NotImplementedError

class NotFoundError(Exception):
  def __init__(self, element, soup):
    super(NotFoundError, self).__init__(
      'Expected %s, but not found (%s)' % (element, soup.prettify()))

class FilterNotFoundError(Exception):
  def __init__(self, msg, soup):
    super(FilterNotFoundError, self).__init__(msg)
    self._soup = soup
    self.write()

  def write(self):
    with open('unparsable.html', 'w') as fh:
      fh.write(self._soup.encode('utf-8'))
