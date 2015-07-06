#!/bin/sh -e

# Bootstrap a development system

pip install -r requirements.txt

sh mkdirs.sh

python django/manage.py migrate

echo Now run: python django/manage.py runserver
