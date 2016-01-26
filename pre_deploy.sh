#!/usr/bin/env bash

cd static && ls && cd ..
rm -rf static/*

tree -p ../uploads
rm -f ../uploads/*.png

python manage.py migrate --delete-ghost-migrations
