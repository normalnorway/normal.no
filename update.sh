#!/bin/sh -e

# Run this on the production server to update the code.

# @todo undo/revert option to check out last good commit

if [ -n "$(git status -s -uno --porcelain)" ]; then
    echo "Aborting! Working tree is not clean:"
    git status -s -uno --porcelain
    exit 1
fi

echo -n commit
git rev-parse live

do_migrate()
{
    sh mkdirs.sh
    django/manage.py migrate
}

do_check()
{
    django/manage.py check

    make -C django/static/css check
    make -C django/static/css
}

do_static()
{
    django/manage.py collectstatic --noinput -i \*.less -i Makefile
    # Note: This will copy more than needed.
}

git pull

if [ x$1 == xfull ];
then
    # Q: if these fail, will script abort?
    do_migrate
    do_check
    do_static
    # make livetest
fi

touch django/website/wsgi.py
