from filters.siat import SiatEntry, SiatListing
from filters.ssss import SsssEntry, SsssListing
from filters.veb import VebEntry, VebListing

ENTRY_FILTERS = [
  SiatEntry(),
  SsssEntry(),
  VebEntry(),
]

ENTRY_LISTINGS = [
  SiatListing(),
  SsssListing(),
  VebListing(),
]
