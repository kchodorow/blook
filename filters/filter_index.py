from filters.siat import SiatEntry, SiatListing, AvcListing, MmmListing, MmmEntry, NhlListing
from filters.ssss import SsssEntry, SsssListing
from filters.veb import VebEntry, VebListing

ENTRY_FILTERS = [
  MmmEntry(),
  SiatEntry(),
  SsssEntry(),
  VebEntry(),
]

ENTRY_LISTINGS = [
  AvcListing(),
  MmmListing(),
  SiatListing(),
  SsssListing(),
  VebListing(),
  NhlListing(), # Uses 'Next Page' for TOC, so must be after 'Previous'.
]
