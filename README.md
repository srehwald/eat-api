# eat-api

[![Build Status](https://travis-ci.org/srehwald/eat-api.svg?branch=master)](https://travis-ci.org/srehwald/eat-api)

Simple static API for the canteens of the [Studentenwerk München](http://www.studentenwerk-muenchen.de) as well as some other locations. By now, the following locations are supported:

| Name                           | API-key                        | Address location                                                                                                       |
|:-------------------------------|:-------------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| Mensa Arcisstraße              | mensa-arcisstr                 | [Arcisstraße 17, München](https://www.google.com/maps?q=Arcisstraße+17,+München)                                       |
| Mensa Garching                 | mensa-garching                 | [Lichtenbergstraße 2, Garching](https://www.google.com/maps?q=Lichtenbergstraße+2,+Garching)                           |
| Mensa Leopoldstraße            | mensa-leopoldstr               | [Leopoldstraße 13a, München](https://www.google.com/maps?q=Leopoldstraße+13a,+München)                                 |
| Mensa Lothstraße               | mensa-lothstr                  | [Lothstraße 13d, München](https://www.google.com/maps?q=Lothstraße+13d,+München)                                       |
| Mensa Martinsried              | mensa-martinsried              | [Großhaderner Straße 6, Planegg-Martinsried](https://www.google.com/maps?q=Großhaderner%20Straße+6,+Planegg-Martinsried) |
| Mensa Pasing                   | mensa-pasing                   | [Am Stadtpark 20, München](https://www.google.com/maps?q=Am%20Stadtpark+20,+München)                                     |
| Mensa Weihenstephan            | mensa-weihenstephan            | [Maximus-von-Imhof-Forum 5, Freising](https://www.google.com/maps?q=Maximus-von-Imhof-Forum+5,+Freising)               |
| StuBistro Arcisstraße          | stubistro-arcisstr             | [Arcisstraße 12, München](https://www.google.com/maps?q=Arcisstraße+12,+München)                                       |
| StuBistro Goethestraße         | stubistro-goethestr            | [Goethestraße 70, München](https://www.google.com/maps?q=Goethestraße+70,+München)                                     |
| StuBistro Großhadern           | stubistro-grosshadern          | [Butenandtstraße 13, Gebäude F, München](https://www.google.com/maps?q=Butenandtstraße+13,+Gebäude+F,+München)         |
| StuBistro Rosenheim            | stubistro-rosenheim            | [Hochschulstraße 1, Rosenheim](https://www.google.com/maps?q=Hochschulstraße+1,+Rosenheim)                             |
| StuBistro Schellingstraße      | stubistro-schellingstr         | [Schellingstraße 3, München](https://www.google.com/maps?q=Schellingstraße+3,+München)                                 |
| StuCafé Adalbertstraße         | stucafe-adalbertstr            | [Adalbertstraße 5, München](https://www.google.com/maps?q=Adalbertstraße+5,+München)                                   |
| StuCafé Akademie Weihenstephan | stucafe-akademie-weihenstephan | [Alte Akademie 1, Freising](https://www.google.com/maps?q=Alte%20Akademie+1,+Freising)                                   |
| StuCafé Boltzmannstraße        | stucafe-boltzmannstr           | [Boltzmannstraße 15, Garching](https://www.google.com/maps?q=Boltzmannstraße+15,+Garching)                             |
| StuCafé in der Mensa Garching  | stucafe-garching               | [Lichtenbergstraße 2, Garching](https://www.google.com/maps?q=Lichtenbergstraße+2,+Garching)                           |
| StuCafé Karlstraße             | stucafe-karlstr                | [Karlstraße 6, München](https://www.google.com/maps?q=Karlstraße+6,+München)                                           |
| StuCafé Pasing                 | stucafe-pasing                 | [Am Stadtpark 20, München](https://www.google.com/maps?q=Am%20Stadtpark+20,+München)                                     |
| FMI Bistro Garching            | fmi-bistro                     | [Boltzmannstraße 3, Garching](https://www.google.com/maps?q=Boltzmannstraße+3,+Garching)                   |
| IPP Bistro Garching            | ipp-bistro                     | [Boltzmannstraße 2, Garching](https://goo.gl/maps/vYdsQhgxFvH2)                   |

## Ingredients list:
<details><summary>CLICK ME</summary>
<p>

```python
ingredient_lookup = {
        "GQB" : "Certified Quality - Bavaria",
        "MSC" : "Marine Stewardship Council",

        "1" : "with dyestuff",
        "2" : "with preservative",
        "3" : "with antioxidant",
        "4" : "with flavor enhancers",
        "5" : "sulphured",
        "6" : "blackened (olive)",
        "7" : "waxed",
        "8" : "with phosphate",
        "9" : "with sweeteners",
        "10" : "contains a source of phenylalanine",
        "11" : "with sugar and sweeteners",
        "13" : "with cocoa-containing grease",
        "14" : "with gelatin",
        "99" : "with alcohol",

        "f" : "meatless dish",
        "v" : "vegan dish",
        "S" : "with pork",
        "R" : "with beef",
        "K" : "with veal",
        "G" : "with poultry", # mediziner mensa
        "W" : "with wild meat", # mediziner mensa
        "L" : "with lamb", # mediziner mensa
        "Kn" : "with garlic",
        "Ei" : "with chicken egg",
        "En" : "with peanut",
        "Fi" : "with fish",
        "Gl" : "with gluten-containing cereals",
        "GlW" : "with wheat",
        "GlR" : "with rye",
        "GlG" : "with barley",
        "GlH" : "with oats",
        "GlD" : "with spelt",
        "Kr" : "with crustaceans",
        "Lu" : "with lupines",
        "Mi" : "with milk and lactose",
        "Sc" : "with shell fruits",
        "ScM" : "with almonds",
        "ScH" : "with hazelnuts",
        "ScW" : "with Walnuts",
        "ScC" : "with cashew nuts",
        "ScP" : "with pistachios",
        "Se" : "with sesame seeds",
        "Sf" : "with mustard",
        "Sl" : "with celery",
        "So" : "with soy",
        "Sw" : "with sulfur dioxide and sulfites",
        "Wt" : "with mollusks",
}
```
Based on: [Studentenwerk München](https://www.studentenwerk-muenchen.de/mensa/speiseplan)

</p>
</details>

## Usage

### API
The actual API is provided by static JSON files, which can be found in the gh-pages branch of this repository. These files are created through automatic travis builds. You need to structure a link as follows in order to access the API:
```
https://srehwald.github.io/eat-api/<location>/<year>/<week-number>.json
```

#### Example
The following link would give you the menu of Mensa Garching for week 9 in 2017:
```
https://srehwald.github.io/eat-api/mensa-garching/2017/09.json
```

### CLI
The JSON files are produced by the tool shown in this repository. Hence, it is either possible to access the API or use the tool itself to obtain the desired menu data. The CLI needs to be used as follows:

```
$ python src/main.py -h
usage: main.py [-h] [-d DATE] [-j PATH] [-c] [--openmensa PATH]
               {fmi-bistro,ipp-bistro,mensa-garching,stucafe-karlstr,mensa-pasing,mensa-arcisstr,
               stucafe-boltzmannstr,stubistro-arcisstr,stucafe-garching,mensa-martinsried,
               mensa-weihenstephan,stubistro-grosshadern,stucafe-akademie-weihenstephan,mensa-lothstr,
               stubistro-goethestr,stubistro-großhadern,mensa-arcisstrasse,stucafe-pasing,
               stubistro-rosenheim,stucafe-adalbertstr,stubistro-schellingstr,mensa-leopoldstr}

positional arguments:
  {fmi-bistro,ipp-bistro,mensa-garching,stucafe-karlstr,mensa-pasing,mensa-arcisstr,
  stucafe-boltzmannstr,stubistro-arcisstr,stucafe-garching,mensa-martinsried,
  mensa-weihenstephan,stubistro-grosshadern,stucafe-akademie-weihenstephan,mensa-lothstr,
  stubistro-goethestr,stubistro-großhadern,mensa-arcisstrasse,stucafe-pasing,
  stubistro-rosenheim,stucafe-adalbertstr,stubistro-schellingstr,mensa-leopoldstr}
                        the location you want to eat at

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  date (DD.MM.YYYY) of the day of which you want to get
                        the menu
  -j PATH, --jsonify PATH
                        directory for JSON output (date parameter will be
                        ignored if this argument is used)
  -c, --combine         creates a "combined.json" file containing all dishes
                        for the location specified
  --openmensa PATH      directory for OpenMensa XML output (date parameter
                        will be ignored if this argument is used)
```

It is mandatory to specify the canteen (e.g. mensa-garching). Furthermore, you can specify a date, for which you would like to get the menu. If no date is provided, all the dishes for the current week will be printed to the command line. the `--jsonify` option is used for the API and produces some JSON files containing the menu data.

#### Example
Here are some sample calls:

```
# Get the menus for the whole current week at mensa-garching
$ python src/main.py mensa-garching

# Get the menu for April 2 at mensa-arcisstrasse
$ python src/main.py mensa-arcisstrasse -d 02.04.2017
```

## Projects using `eat-api`

- Parser for [OpenMensa](https://openmensa.org) ([GitHub](https://github.com/openmensa/openmensa))
  - [Wilhelm Gastronomie im FMI Gebäude der TUM Garching](https://openmensa.org/c/773)
  - [Konradhofer Catering - Betriebskantine IPP](https://openmensa.org/c/774)
- [Hunger | TUM.sexy](http://tum.sexy/hunger/) ([Github](https://github.com/mammuth/TUM.sexy))
- `FMeat.php` SDK ([GitHub](https://github.com/jpbernius/fmeat.php))
- [Telegram](https://telegram.org/) bot for [Channel t.me/lunchgfz](https://t.me/lunchgfz) ([GitLab](https://gitlab.com/raabf/lunchgfz-telegram))
- UWP-TUM-Campus-App ([Github](https://github.com/COM8/UWP-TUM-Campus-App))
