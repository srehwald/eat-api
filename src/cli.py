# -*- coding: utf-8 -*-

import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('location', choices=['mensa-garching'], help='the location you want to eat at')
    parser.add_argument('-d', '--date', help='date (DD.MM.YYYY) of the day of which you want to get the menu')
    parser.add_argument('-j', '--jsonify',
                        help="if this flag is set, the parsing results will be put into a particular folder structure "
                             "and converted to JSON so that it can be used for a static API", action='store_true')
    args = parser.parse_args()
    return args
