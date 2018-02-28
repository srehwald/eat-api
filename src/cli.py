# -*- coding: utf-8 -*-

import argparse

import menu_parser


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('location', choices=(
            ['fmi-bistro', 'ipp-bistro'] + list(menu_parser.StudentenwerkMenuParser.location_id_mapping.keys())),
                        help='the location you want to eat at')
    parser.add_argument('-d', '--date', help='date (DD.MM.YYYY) of the day of which you want to get the menu')
    parser.add_argument('-j', '--jsonify',
                        help="directory for JSON output (date parameter will be ignored if this argument is used)",
                        metavar="PATH")
    parser.add_argument('-c', '--combine', action='store_true',
                        help='creates an "combined.json", containing all available dishes for the location')
    args = parser.parse_args()
    return args
