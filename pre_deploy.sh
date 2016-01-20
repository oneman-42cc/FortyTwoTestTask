#!/usr/bin/env bash

tree -p .static
cd static && ls && cd ..
rm -rf static/*
