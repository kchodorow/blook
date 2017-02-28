from cache import Cache

import unittest

class CacheTest(unittest.TestCase):
  def test_absolute_url(self):
    c = Cache('http://www.example.com/blog')
    input_url = 'http://other-url.biz'
    output_url = c.get_full_url(input_url)
    self.assertEqual(input_url, output_url)

  def test_url_from_root(self):
    c = Cache('http://www.example.com/blog')
    input_url = '/foo'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/foo', output_url)

  def test_url_from_original_root(self):
    c = Cache('http://www.example.com')
    input_url = '/foo'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/foo', output_url)

  def test_query_url(self):
    c = Cache('http://www.example.com/blog?page1')
    input_url = '?page2'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/blog?page2', output_url)

  def test_add_query_to_url(self):
    c = Cache('http://www.example.com/blog')
    input_url = '?page2'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/blog?page2', output_url)

  def test_relative_url(self):
    c = Cache('http://www.example.com/blog/page1')
    input_url = 'page2'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/blog/page2', output_url)

  def test_relative_url_from_base(self):
    c = Cache('http://www.example.com')
    input_url = 'blog'
    output_url = c.get_full_url(input_url)
    self.assertEqual('http://www.example.com/blog', output_url)

if __name__ == '__main__':
  unittest.main()
