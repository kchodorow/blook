from filters.siat import SiatEntry, SiatListing, AvcListing
from filters.ssss import SsssEntry, SsssListing
from filters.veb import VebEntry, VebListing

ENTRY_FILTERS = [
  SiatEntry(),
  SsssEntry(),
  VebEntry(),
]

ENTRY_LISTINGS = [
  AvcListing(),
  SiatListing(),
  SsssListing(),
  VebListing(),
]
