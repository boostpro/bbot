#
# Get bbot into the path.  This part wouldn't be needed in an ordinary
# project, but this test project is of course part of the bbot source
# distribution, so the source for bbot itself is above here.
#
import sys
from os.path import dirname as pdir
_bbot_parent_dir = pdir(pdir(pdir(pdir(__file__))))
if _bbot_parent_dir not in sys.path:
    sys.path.insert(0, _bbot_parent_dir)

