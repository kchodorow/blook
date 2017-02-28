# Blook

Blook is a tool for turning blogs into ebooks. GIve blook a blog's URL and it'll
create a .epub from the content.

## Install

Clone this repo and install the prerequisites:

```
$ git clone https://github.com/kchodorow/blook.git
$ pip install beautifulsoup4 ebooklib
```

## Usage

To use, specify the 'main' url of the blog, e.g.:

```
$ python blook.py http://avc.com/
```

If you only want the latest N entries (for example, you're downloading a very
large blog and you don't actually want all of the entries) you can give a limit:

```
$ python blook.py --limit 73 avc.com
```

This would download the last 73 entries.

## What if a blog isn't parsed correctly?

If you find a blog that this does not parse correctly, please [file an
issue](https://github.com/kchodorow/blook/issues).

Alternatively, please feel free to add a new blog format:

* Add a file to [filters/](https://github.com/kchodorow/blook/tree/master/filters).
* Extend `base.BaseEntry` and `base.BaseListing` with the appropriate code (use
  [siat.py](https://github.com/kchodorow/blook/tree/master/filters/siat.py) as
  an example).
* Add your filter to [the filter
  list](https://github.com/kchodorow/blook/tree/master/filters/filter_index.py).
* Add some tests to `filters/your_filter_test.py` following the
  `extract/extractor_test.py` model. Create test HTML files as needed in
  `filters/test_data/`. TODO: come up with more comprehensive
  template-specific tests and put them in the filters/ directory.
* Make sure your test passes by running `python -m filters.your_filter_test`.
* Submit a pull request!
