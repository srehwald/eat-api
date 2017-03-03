# -*- coding: utf-8 -*-

import cli
import menu_parser
from datetime import date, datetime


def get_menu_parsing_strategy(location):
    parser = None

    # set parsing strategy based on location
    if location == "mensa-garching":
        parser = menu_parser.StudentenwerkMenuParser()

    return parser


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

    # date is by default today's date
    menu_date = date.today()
    # if date has been explicitly specified, try to parse it
    if args.date is not None:
        try:
            menu_date = datetime.strptime(args.date, '%d.%m.%Y').date()
        except ValueError:
            print("Incorrect date format; should be DD.MM.YYYY!")
            return

    # print menu if available
    if menus is None:
        print("Parsing error.")
    elif args.date is not None:
        if menu_date not in menus:
            print("There is no menu for '%s' on %s!" % (location, menu_date))
            return
        menu = menus[menu_date]
        print(menu)
    else:
        for menu in menus:
            print(menus[menu])


if __name__ == "__main__":
    main()
