# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from lxml import html
from datetime import date

import main
from menu_parser import StudentenwerkMenuParser
from entities import Dish, Menu, Week
import json


class StudentenwerkMenuParserTest(unittest.TestCase):
    studentenwerk_menu_parser = StudentenwerkMenuParser()

    menu_html = html.fromstring(
        open("src/test/assets/speiseplan_garching.html").read())
    menu_html_wrong_date_format = html.fromstring(
        open("src/test/assets/speiseplan_garching_wrong_date_format.html").read())

    dish1_1 = Dish("Kartoffelgulasch mit Paprika", 1)
    dish1_2 = Dish("Hackfleischbällchen mit Champignonrahmsauce", 1.9)
    dish1_3 = Dish("Seelachsfilet (MSC) im Sesammantel mit Remouladensauce", 2.4)
    dish1_4 = Dish("Gebackene Calamari-Ringe mit Remouladensauce", 2.6)

    dish2_1 = Dish("Kartoffeleintopf mit Majoran", 1)
    dish2_2 = Dish("Gulasch vom Schwein", 1.9)
    dish2_3 = Dish("Paniertes Hähnchenschnitzel", 2.4)

    menu1_date = date(2017, 3, 27)
    menu2_date = date(2017, 4, 3)

    menu1 = Menu(menu1_date, [dish1_1, dish1_2, dish1_3, dish1_4])
    menu2 = Menu(menu2_date, [dish2_1, dish2_2, dish2_3])

    def test_Should_ReturnMenu_When_PassedDateIsCorrect(self):
        self.assertEqual(self.menu1, self.studentenwerk_menu_parser.get_menus(self.menu_html)[self.menu1_date])
        self.assertEqual(self.menu2, self.studentenwerk_menu_parser.get_menus(self.menu_html)[self.menu2_date])

    def test_Should_IgnoreDay_When_DateOfTheDayIsInAWrongFormat(self):
        self.assertEqual(22, len(self.studentenwerk_menu_parser.get_menus(self.menu_html_wrong_date_format)))

    def test_Should_ReturnWeeks_When_ConvertingMenuToWeekObjects(self):
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html)
        weeks_actual = Week.to_weeks(menus)
        length_weeks_actual = len(weeks_actual)

        self.assertEqual(5, length_weeks_actual)
        for calendar_week in weeks_actual:
            week = weeks_actual[calendar_week]
            week_length = len(week.days)
            # calendar weeks 15 and 16 have one day less, because of a holiday
            if calendar_week == 15 or calendar_week == 16:
                self.assertEqual(4, week_length)
            else:
                self.assertEqual(5, week_length)

    def test_Should_ConvertWeekToJSON(self):
        with open('src/test/assets/speiseplan_garching_kw2017-13.json') as data_file:
            week_2017_13 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2017-14.json') as data_file:
            week_2017_14 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2017-15.json') as data_file:
            week_2017_15 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2017-16.json') as data_file:
            week_2017_16 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2017-17.json') as data_file:
            week_2017_17 = json.load(data_file)

        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html)
        weeks = Week.to_weeks(menus)
        week_2017_13_actual = json.loads(weeks[13].to_json())
        week_2017_14_actual = json.loads(weeks[14].to_json())
        week_2017_15_actual = json.loads(weeks[15].to_json())
        week_2017_16_actual = json.loads(weeks[16].to_json())
        week_2017_17_actual = json.loads(weeks[17].to_json())

        self.assertEqual(sorted(week_2017_13_actual.items()), sorted(week_2017_13.items()))
        self.assertEqual(sorted(week_2017_14_actual.items()), sorted(week_2017_14.items()))
        self.assertEqual(sorted(week_2017_15_actual.items()), sorted(week_2017_15.items()))
        self.assertEqual(sorted(week_2017_16_actual.items()), sorted(week_2017_16.items()))
        self.assertEqual(sorted(week_2017_17_actual.items()), sorted(week_2017_17.items()))

    def test_Should_CreateCorrectDirectoriesAndJSONFiles(self):
        # parse menu
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html)
        # get weeks
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            main.jsonify(weeks, temp_dir)

            # check if two directories are created (one for 2016 and 2017)
            created_dirs = [name for name in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, name))]
            created_dirs.sort()
            self.assertEqual(1, len(created_dirs))
            self.assertEqual("2017", created_dirs[0])

            # check if the created directories contain the JSON files
            dir_2017 = "%s/2017" % temp_dir
            files_in_2017 = [name for name in os.listdir(dir_2017) if os.path.isfile(os.path.join(dir_2017, name))]
            files_in_2017.sort()
            self.assertEqual(["13.json", "14.json", "15.json", "16.json", "17.json"], files_in_2017)
