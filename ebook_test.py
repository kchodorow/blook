from bs4 import BeautifulSoup
from cache import PageNotFoundError
from ebook import Ebook
from extract.extractor import ListingNotFoundError

import os
import unittest

class EbookTest(unittest.TestCase):
  INDEX = """
<html>
  <head>
    <title>Nhl</title>
  </head>
  <body>
    <article><h2><a href="http://www.examle.com/post1/">Post 1</a></h2></article>
    <article><h2><a href="http://www.examle.com/post2/">Post 2</a></h2></article>
    <article><h2><a href="http://www.examle.com/post3/">Post 3</a></h2></article>
    <a href="http://www.example.com/page/2/">Next Page »</a>
  </body>
</html>
"""

  NON_INDEX = """
<html>
  <head>
    <title>Non page</title>
  </head>
  <body>
  </body>
</html>
"""

  def tearDown(self):
    if os.path.exists('Nhl.epub'):
      os.remove('Nhl.epub')
    if os.path.exists('unparseable.html'):
      os.remove('unparsable.html')

  def test_assemble(self):
    cache = TestCache()
    cache.put('https://www.example.com', self.INDEX)
    ebook = Ebook('https://www.example.com', 2, cache)
    ebook.assemble()
    self.assertEqual('Nhl', ebook.get_title())
    self.assertEqual('Nhl.epub', ebook.get_filename())

  def test_redirect(self):
    cache = TestCache()
    cache.put('https://www.example.com', self.NON_INDEX)
    cache.put('https://www.example.com/blog', self.INDEX)
    ebook = Ebook('https://www.example.com', 10, cache)
    ebook.assemble()
    self.assertEqual('Nhl', ebook.get_title())
    self.assertEqual('Nhl.epub', ebook.get_filename())

  def test_no_redirect(self):
    cache = TestCache()
    cache.put('https://www.example.com/blog', self.NON_INDEX)
    ebook = Ebook('https://www.example.com/blog', 10, cache)
    try:
      ebook.assemble()
      self.fail('Expected ebook.assemble to throw')
    except ListingNotFoundError, expected:
      self.assertEqual('No listing filter found', expected.message)
    with open('unparsable.html', 'r') as fh:
      unparsable = fh.read()
    self.assertEqual(
      str(BeautifulSoup(self.NON_INDEX, 'html.parser')), unparsable)

class TestCache(object):
  def __init__(self):
    self._map = {}

  def put(self, url, content):
    self._map[url] = content

  def get(self, url):
    if url in self._map:
      return self._map[url]
    return ""

if __name__ == '__main__':
  unittest.main()
