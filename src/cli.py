# -*- coding: utf-8 -*-

import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('location', choices=['mensa-garching', 'mensa-arcisstrasse', 'stubistro-grosshadern',
                                             'fmi-bistro'],
                        help='the location you want to eat at')
    parser.add_argument('-d', '--date', help='date (DD.MM.YYYY) of the day of which you want to get the menu')
    parser.add_argument('-j', '--jsonify',
                        help="directory for JSON output (date parameter will be ignored if this argument is used)",
                        metavar="PATH")
    args = parser.parse_args()
    return args
