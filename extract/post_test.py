from post import Entry

import ebook
import unittest

class PostTest(unittest.TestCase):
  def test_extract_siat(self):
    with open('extract/test/snail_entry.html', 'r') as fh:
      page = fh.read()
    post = Entry(page, ebook.ENTRY_FILTERS)
    chapter = post.get_epub_chapter()
    self.assertEquals('Title 1', chapter.title)
    self.assertEquals('Title-1.xhtml', chapter.file_name)
    self.assertEquals(
      '<div class="entrytext">I\'m some content</div>', chapter.content)

if __name__ == '__main__':
  unittest.main()
