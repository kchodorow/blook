import re

def title_to_filename(title):
  title = title.replace(' ', '-')
  return re.sub(r'[^-A-Za-z0-9_]', '', title)

def generate_uid(title):
  return re.sub(r'[^A-Za-z0-9_]', '', title)
