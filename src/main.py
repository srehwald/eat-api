# -*- coding: utf-8 -*-
import json
import os

import cli
import menu_parser

import util
from openmensa import openmensa
from entities import Week


def get_menu_parsing_strategy(location):
    parser = None

    # set parsing strategy based on location
    if isinstance(location, int) or location in menu_parser.StudentenwerkMenuParser.location_id_mapping.keys():
        parser = menu_parser.StudentenwerkMenuParser()
    elif location == "fmi-bistro":
        parser = menu_parser.FMIBistroMenuParser()
    elif location == "ipp-bistro":
        parser = menu_parser.IPPBistroMenuParser()

    return parser


def jsonify(weeks, directory, location, combine_dishes):
    # iterate through weeks
    for calendar_week in weeks:
        # get Week object
        week = weeks[calendar_week]
        # get year of calendar week
        year = week.year

        # create dir: <year>/
        json_dir = "%s/%s" % (str(directory), str(year))
        if not os.path.exists(json_dir):
            os.makedirs("%s/%s" % (str(directory), str(year)))

        # convert Week object to JSON
        week_json = week.to_json()
        # write JSON to file: <year>/<calendar_week>.json
        with open("%s/%s.json" % (str(json_dir), str(calendar_week).zfill(2)), 'w') as outfile:
            json.dump(json.loads(week_json), outfile, indent=4, ensure_ascii=False)

    # check if combien parameter got set
    if not combine_dishes:
        return
    # the name of the output directory and file
    combined_df_name = 'combined'

    # create directory for combined output
    json_dir = "%s/%s" % (str(directory), combined_df_name)
    if not os.path.exists(json_dir):
        os.makedirs("%s/%s" % (str(directory), combined_df_name))

    # convert all weeks to one JSON object
    weeks_json_all = json.dumps(
        {"canteen_id": location, "weeks": [weeks[calendar_week].to_json_obj() for calendar_week in weeks]}, 
        ensure_ascii=False, indent=4)
    
    # write JSON object to file
    with open("%s/%s.json" % (str(json_dir), combined_df_name), 'w') as outfile:
        json.dump(json.loads(weeks_json_all), outfile, indent=4, ensure_ascii=False)


def main():
    # get command line args
    args = cli.parse_cli_args()

    # get location from args
    location = args.location
    # get required parser
    parser = get_menu_parsing_strategy(location)
    if parser is None:
        print("The selected location '%s' does not exist." % location)

    # parse menu
    menus = parser.parse(location)

    # if date has been explicitly specified, try to parse it
    menu_date = None
    if args.date is not None:
        try:
            menu_date = util.parse_date(args.date)
        except ValueError as e:
            print("Error during parsing date from command line: %s" % args.date)
            print("Required format: %s" % util.cli_date_format)
            return

    # print menu
    if menus is None:
        print("Error. Could not retrieve menu(s)")
    # jsonify argument is set
    elif args.jsonify is not None:
        weeks = Week.to_weeks(menus)
        if not os.path.exists(args.jsonify):
            os.makedirs(args.jsonify)
        jsonify(weeks, args.jsonify, location, args.combine)
    elif args.openmensa is not None:
        weeks = Week.to_weeks(menus)
        if not os.path.exists(args.openmensa):
            os.makedirs(args.openmensa)
        openmensa(weeks, args.openmensa)
    # date argument is set
    elif args.date is not None:
        if menu_date not in menus:
            print("There is no menu for '%s' on %s!" % (location, menu_date))
            return
        menu = menus[menu_date]
        print(menu)
    # else, print weeks
    else:
        weeks = Week.to_weeks(menus)
        for calendar_week in weeks:
            print(weeks[calendar_week])


if __name__ == "__main__":
    main()
