# -*- coding: utf-8 -*-

import cli
import menu_parser

import util


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
