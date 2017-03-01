from bs4 import BeautifulSoup
from siat import NhlListing

import unittest

class NhlListingTest(unittest.TestCase):
  CONTENT = BeautifulSoup("""
<html>
  <head>
    <title>Nhl</title>
  </head>
  <body>
    <article><h2><a href="http://www.examle.com/post1/">Post 1</a></h2></article>
    <article><h2><a href="http://www.examle.com/post2/">Post 2</a></h2></article>
    <a href="http://www.example.com/page/2/">Next Page »</a>
  </body>
</html>""", 'html.parser')

  def test_applies(self):
    listing = NhlListing()
    self.assertTrue(listing.applies(self.CONTENT))

  def test_urls(self):
    listing = NhlListing()
    urls = listing.extract_urls(self.CONTENT)
    self.assertEqual(2, len(urls))
    self.assertEqual('http://www.examle.com/post1/', urls[0])
    self.assertEqual('http://www.examle.com/post2/', urls[1])

  def test_next_page(self):
    listing = NhlListing()
    url = listing.next_page_url(self.CONTENT)
    self.assertTrue('http://www.example.com/page/2/', url)

if __name__ == '__main__':
  unittest.main()
