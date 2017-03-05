#!/bin/sh
mkdir dist
python src/main.py mensa-garching -j ./dist/mensa-garching
tree dist/