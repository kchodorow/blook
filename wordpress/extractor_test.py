from bs4 import BeautifulSoup
from extractor import Extractor

import unittest

class ExtractorTest(unittest.TestCase):
  def test_extract(self):
    with open('wordpress/test/snail.html', 'r') as fh:
      index = fh.read()
    page = BeautifulSoup(index, 'html.parser')
    cache = TestCache()
    extractor = Extractor(page, cache)
    urls = extractor.extract(0)
    self.assertEqual('https://www.example.com/title1', urls[0])
    self.assertEqual('https://www.example.com/title2', urls[1])
    self.assertEqual('https://www.example.com/title3', urls[2])

class TestCache(object):
  def get(self, url):
    return None

  def put(self, url, content):
    pass

if __name__ == '__main__':
  unittest.main()
