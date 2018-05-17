#!/usr/bin/env bash
# bin/detect <build-dir>

if [ -f $1/package.json ]; then
  echo 'Node.js'
  exit 0
fi

>&2 echo 'Node.js: package.json not found in application root'
exit 1