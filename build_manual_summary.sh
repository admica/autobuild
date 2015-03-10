#!/bin/sh

if [ $# != 1 ]; then
  echo "-+-"
  echo "Purpose:"
  echo "* Build the summary html page manually using the most recent build."
  echo "-+-"
  echo "Directly Modifies:"
  echo "* /export/home/autobuild/autobuild.<arch>/<arch>_build.html"
  echo "-+-"
  echo "Usage: $0 <arch>"
  echo "-+-"
  exit 1
fi 

./build_summary.py $1 \
    /export/home/autobuild/autobuild.$1/nightly0.txt \
    /export/home/autobuild/autobuild.$1/nightly1.txt \
    /export/home/autobuild/autobuild.$1/nightly2.txt \
    /export/home/autobuild/autobuild.$1/nightly3.txt \
    /export/home/autobuild/autobuild.$1/nightly4.txt \
    /export/home/autobuild/autobuild.$1/nightly5.txt \
    /export/home/autobuild/autobuild.$1/nightly6.txt \
    /export/home/autobuild/autobuild.$1/nightly7.txt > /export/home/autobuild/autobuild.$1/$1_build.html
