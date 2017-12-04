#!/bin/bash

# --parents prevents error exit if folder already exists
mkdir --parents dist

loc_list=( "mensa-arcisstr" "mensa-arcisstrasse" "mensa-garching" "mensa-leopoldstr" "mensa-lothstr" \
"mensa-martinsried" "mensa-pasing" "mensa-weihenstephan" "stubistro-arcisstr" "stubistro-goethestr" \
"stubistro-großhadern" "stubistro-grosshadern" "stubistro-rosenheim" "stubistro-schellingstr" "stucafe-adalbertstr" \
"stucafe-akademie-weihenstephan" "stucafe-boltzmannstr" "stucafe-garching" "stucafe-karlstr" "stucafe-pasing" \
"ipp-bistro" "fmi-bistro" )

for loc in "${loc_list[@]}"; do
    python src/main.py "$loc" --jsonify "./dist/$loc"
done

tree dist/
