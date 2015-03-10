#!/bin/sh
#
#  checkout_and_build.sh
#
# This worker script checks out a software system from a specifiec Subversion
#   location into a specified target location and performs a full build of it.
#   (i.e. it invokes ./buildAll.sh)
#

SVN_LOCATION=$1
TARGET_DIR=$2

echo "Checking out software from ${SVN_LOCATION} into into ${TARGET_DIR}"
svn checkout ${SVN_LOCATION} ${TARGET_DIR}

echo "Building Software..."
if [ -z "${DISPLAY}" ]; then
    export DISPLAY=:0
fi
cd ${TARGET_DIR}
./buildAll.sh
