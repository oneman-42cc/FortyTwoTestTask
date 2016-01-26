#!/usr/bin/env bash

now="$(date +'%Y%m%d-%H%m')"
MANAGE=manage.py

python $MANAGE projectmodels --stream=stderr 2>> $now.dat