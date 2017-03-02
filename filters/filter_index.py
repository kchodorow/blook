from filters.siat import SiatEntry, SiatListing, AvcListing, MmmListing, MmmEntry, NhlListing, LackhandEntry, LackhandListing
from filters.ssss import SsssEntry, SsssListing
from filters.veb import VebEntry, VebListing

ENTRY_FILTERS = [
  LackhandEntry(),
  MmmEntry(),
  SiatEntry(),
  SsssEntry(),
  VebEntry(),
]

ENTRY_LISTINGS = [
  AvcListing(),
  LackhandListing(),
  MmmListing(),
  SiatListing(),
  SsssListing(),
  VebListing(),
  NhlListing(), # Uses 'Next Page' for TOC, so must be after 'Previous'.
]
