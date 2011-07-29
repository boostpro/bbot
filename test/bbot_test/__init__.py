#
# Get bbot into the path.  This part wouldn't be needed in an ordinary
# project, but this test project is of course part of the bbot source
# distribution, so the source for bbot itself is above here.
#
import sys, os
from os.path import dirname as pdir
sys.path.append(pdir(pdir(pdir(pdir(__file__)))))

