#!/bin/sh
# Creates a tarball for autobuild releases.

if [ $# != 1 ]; then
  echo "-+-"
  echo "Purpose:"
  echo "* Create a tarball for autobuild releases."
  echo "-+-"
  echo "Usage: $0 <tar.gz to create>"
  echo "-+-"
  exit 1
fi 

tar -czvf $1 \
  build_log.py \
  build_manual_log.sh \
  build_manual_summary.sh \
  build_smtp.py \
  build_summary.py \
  build.sh \
  checkout_and_build.sh \
  autobuild.ppc \
  autobuild.x86_64 \
  autobuild.readme.txt \
  autobuild.make.archive.sh \
  /etc/cron.daily/autobuild
