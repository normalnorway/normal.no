#!/bin/sh -e

## Git Submodules
git submodule init
git submodule update
# Note: Submodules are check out in a detached state:
#(cd django/apps/news/newsgrab && git co master)

## Fetch (test) database
if [ ! -e db/normal.db ]; then
    echo "Fetching db/normal.db"
    (cd db && wget --quiet http://torkel.normal.no/normal.db)
fi

## Create directories
mkdir -p logs
