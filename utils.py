import re

def title_to_filename(title):
  title = title.replace(' ', '-')
  return "%s" % re.sub(r'[^-A-Za-z0-9_]', '', title)
