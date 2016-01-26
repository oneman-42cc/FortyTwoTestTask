#!/usr/bin/env bash

MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings

cd static && ls && cd ..
rm -rf static/*

tree -p ../uploads
rm -f ../uploads/*.png

PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$SETTINGS $MANAGE migrate --delete-ghost-migrations
