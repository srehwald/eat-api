#!/bin/sh
mkdir dist
python src/main.py mensa-garching -j ./dist/mensa-garching
python src/main.py mensa-arcisstrasse -j ./dist/mensa-arcisstrasse
python src/main.py stubistro-grosshadern -j ./dist/stubistro-grosshadern
python src/main.py fmi-bistro -j ./dist/fmi-bistro
tree dist/