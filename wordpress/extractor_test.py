from bs4 import BeautifulSoup
from extractor import Extractor

import unittest

class ExtractorTest(unittest.TestCase):
  def test_extract(self):
    extractor = Extractor(
      self._get_soup('wordpress/test/snail.html'), TestCache())
    urls = extractor.extract(0)
    self.assertEqual('https://www.example.com/title1', urls[0])
    self.assertEqual('https://www.example.com/title2', urls[1])
    self.assertEqual('https://www.example.com/title3', urls[2])

  def test_limit(self):
    extractor = Extractor(
      self._get_soup('wordpress/test/snail.html'), TestCache())
    urls = extractor.extract(2)
    self.assertEqual(2, len(urls))
    self.assertEqual('https://www.example.com/title1', urls[0])
    self.assertEqual('https://www.example.com/title2', urls[1])

  def _get_soup(self, path):
    with open(path, 'r') as fh:
      index = fh.read()
    return BeautifulSoup(index, 'html.parser')


class TestCache(object):
  def get(self, url):
    return None

  def put(self, url, content):
    pass

if __name__ == '__main__':
  unittest.main()
