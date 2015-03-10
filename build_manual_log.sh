#!/bin/sh

if [ $# != 1 ]; then
  echo "-+-"
  echo "Purpose:"
  echo "* Build the log html pages manually using the most recent build."
  echo "-+-"
  echo "Directly Modifies:"
  echo "* /export/home/autobuild/autobuild.<arch>/<arch>_build.log_x.html"
  echo "-+-"
  echo "Usage: $0 <arch>"
  echo "-+-"
  exit 1
fi 

for x in 0 1 2 3 4 5 6 7; do
  ./build_log.py /export/builds/autobuild/$1/nightly$x/build.log /export/home/autobuild/autobuild.$1/$1_build.log_$x.html
done
