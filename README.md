# stwm-mensa-api

[![Build Status](https://travis-ci.com/srehwald/stwm-mensa-api.svg?token=YUmexXqP9AGj9wNMuDhx&branch=master)](https://travis-ci.com/srehwald/stwm-mensa-api)

Simple static API for the canteens of the [Studentenwerk München](http://www.studentenwerk-muenchen.de). By now, the following locations are supported:
- Mensa Garching
- Mensa Arcisstraße
- StuBistro Großhadern

## Usage

### API
The actual API is provided by static JSON files, which can be found in the gh-pages branch of this repository. These files are created through automatic travis builds.

### CLI
The JSON files are produced by the tool shown in this repository. Hence, it is either possible to access the API or use the tool itself to obtain the desired menu data. The CLI needs to be used as follows:
```
$ python src/main.py -h
usage: main.py [-h] [-d DATE] [-j PATH]
               {mensa-garching,mensa-arcisstrasse,stubistro-grosshadern}

positional arguments:
  {mensa-garching,mensa-arcisstrasse,stubistro-grosshadern}
                        the location you want to eat at

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  date (DD.MM.YYYY) of the day of which you want to get
                        the menu
  -j PATH, --jsonify PATH
                        directory for JSON output (date parameter will be
                        ignored if this argument is used)
```
It is mandatory to specify the canteen (e.g. mensa-garching). Furthermore, you can specify a date, for which you would like to get the menu. If no date is provided, all the dishes for the current week will be printed to the command line. the `--jsonify` option is used for the API and produces some JSON files containing the menu data. Here are some sample calls:
```
# Get the menus for the whole current week at mensa-garching
$ python src/main.py mensa-garching

# Get the menu for April 2 at mensa-arcisstrasse
$ python src/main.py mensa-arcisstrasse -d 02.04.2017
```

# License