#!/bin/sh
#
# The first test attempts to model the actual running configuration
# that we'll use if we want to keep BuildBot's droppings out of our
# source tree: a symlink to master.cfg in the parent directory.  See
# __init__.py for more details about the reasons for this

set -e

buildbot create-master

buildbot start
sleep 1
buildbot reconfig || echo '************** RECONFIG FAILED ***************'
sleep 1
buildbot stop

# Clean up the source directory
rm -rf *.sample public_html state.sqlite twistd.log buildbot.tac

# It's also desirable to be able to run checkconfig directly from the
# root of the source tree during development, using an unmodified
# source tree and adding no symlinks, so we'll test again.
echo '#################'

cd bbot_test
buildbot checkconfig

