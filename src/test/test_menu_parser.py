# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from lxml import html
from datetime import date

import main
from menu_parser import StudentenwerkMenuParser, FMIBistroMenuParser, IPPBistroMenuParser
from entities import Dish, Menu, Week
import json


class StudentenwerkMenuParserTest(unittest.TestCase):
    studentenwerk_menu_parser = StudentenwerkMenuParser()

    menu_html_garching = html.fromstring(
        open("src/test/assets/speiseplan_garching.html").read())
    menu_html_arcisstrasse = html.fromstring(
        open("src/test/assets/speiseplan_arcisstrasse.html").read())
    menu_html_großhadern = html.fromstring(
        open("src/test/assets/speiseplan_großhadern.html").read())
    menu_html_wrong_date_format = html.fromstring(
        open("src/test/assets/speiseplan_garching_wrong_date_format.html").read())

    menu1_date = date(2017, 3, 27)
    menu2_date = date(2017, 4, 3)
    menu3_date = date(2017, 4, 4)

    # dishes in Garching
    dish1_1_garching = Dish("Kartoffelgulasch mit Paprika", 1)
    dish1_2_garching = Dish("Hackfleischbällchen mit Champignonrahmsauce", 1.9)
    dish1_3_garching = Dish("Seelachsfilet (MSC) im Sesammantel mit Remouladensauce", 2.4)
    dish1_4_garching = Dish("Gebackene Calamari-Ringe mit Remouladensauce", 2.6)

    dish2_1_garching = Dish("Kartoffeleintopf mit Majoran", 1)
    dish2_2_garching = Dish("Gulasch vom Schwein", 1.9)
    dish2_3_garching = Dish("Paniertes Hähnchenschnitzel", 2.4)

    menu1_garching = Menu(menu1_date, [dish1_1_garching, dish1_2_garching, dish1_3_garching, dish1_4_garching])
    menu2_garching = Menu(menu2_date, [dish2_1_garching, dish2_2_garching, dish2_3_garching])

    # dishes in Arcisstrasse
    dish1_1_arcisstrasse = Dish("Kartoffelgulasch mit Paprika", 1)
    dish1_2_arcisstrasse = Dish("Hackfleischbällchen mit Champignonrahmsauce", 1.55)
    dish1_3_arcisstrasse = Dish("Hackfleischbällchen mit Champignonrahmsauce (2)", 1.9)
    dish1_4_arcisstrasse = Dish("Pasta Pomodori", 1.9)
    dish1_5_arcisstrasse = Dish("Gebackene Calamari-Ringe mit Zitronen-Knoblauch-Dip", 2.6)
    dish1_6_arcisstrasse = Dish("Seelachsfilet (MSC) im Sesammantel mit Zitronen-Knoblauch-Dip", 2.6)
    dish1_7_arcisstrasse = Dish("Pasta Pomodori (2)", "Self-Service")
    dish1_8_arcisstrasse = Dish("Kartoffelgulasch mit Paprika (2)", "Self-Service")
    dish1_9_arcisstrasse = Dish("Pasta mit Sojabolognese", "Self-Service")
    menu1_arcisstrasse = Menu(menu1_date, [dish1_1_arcisstrasse, dish1_2_arcisstrasse, dish1_3_arcisstrasse,
                                           dish1_4_arcisstrasse, dish1_5_arcisstrasse, dish1_6_arcisstrasse,
                                           dish1_7_arcisstrasse, dish1_8_arcisstrasse, dish1_9_arcisstrasse])

    # dishes in Großhadern
    dish1_1_großhadern = Dish("Pasta-Gemüse-Auflauf mit Tomatensauce", 1.9)
    dish1_2_großhadern = Dish("Rinderroulade nach Hausfrauenart mit Senf-Gemüse-Sauce", 3)
    menu1_großhadern = Menu(menu3_date, [dish1_1_großhadern, dish1_2_großhadern])

    def test_Should_ReturnMenu_When_PassedDateIsCorrect(self):
        self.assertEqual(self.menu1_garching,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)[self.menu1_date])
        self.assertEqual(self.menu2_garching,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)[self.menu2_date])

        self.assertEqual(self.menu1_arcisstrasse,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_arcisstrasse)[self.menu1_date])

        self.assertEqual(self.menu1_großhadern,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_großhadern)[self.menu3_date])

    def test_Should_IgnoreDay_When_DateOfTheDayIsInAWrongFormat(self):
        self.assertEqual(22, len(self.studentenwerk_menu_parser.get_menus(self.menu_html_wrong_date_format)))

    def test_Should_ReturnWeeks_When_ConvertingMenuToWeekObjects(self):
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)
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

        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)
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
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)
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


class FMIBistroParserTest(unittest.TestCase):
    bistro_parser = FMIBistroMenuParser()
    test_menu1 = open('src/test/assets/fmi/Garching-Speiseplan_KW44_2017.txt', 'r').read()
    year1 = 2017
    week_number1 = 44
    test_menu2 = open('src/test/assets/fmi/Garching-Speiseplan_KW45_2017.txt', 'r').read()
    year2 = 2017
    week_number2 = 45

    date_mon1 = date(2017, 10, 30)
    date_thu1 = date(2017, 11, 2)
    date_fri1 = date(2017, 11, 3)
    dish1_mon1 = Dish("Kurkumareis mit Asia Wokgemüse", 3.6)
    dish2_mon1 = Dish("Kartoffel „Cordon Bleu“ mit Frischkäse gefüllt dazu Blattsalate", 4.3)
    dish3_mon1 = Dish("Putenschnitzel natur mit Paprikarahmsoße dazu Ebly Gemüseweizen", 5.3)
    dish1_thu1 = Dish("Süßkartoffel Gemüsepfanne", 3.6)
    dish2_thu1 = Dish("Gemüse Nudelauflauf", 4.3)
    dish3_thu1 = Dish("Hähnchenspieß in Kokos Currysoße dazu Früchtereis", 5.3)
    dish1_fri1 = Dish("Antipasti Rosmarinkartoffeln", 3.6)
    dish2_fri1 = Dish("Schlemmerfilet auf Antipasti Rosmarinkartoffeln", 4.5)
    dish3_fri1 = Dish("Kaiserschmarrn mit Zwetschenröster", 3)
    menu_mon1 = Menu(date_mon1, [dish1_mon1, dish2_mon1, dish3_mon1])
    menu_thu1 = Menu(date_thu1, [dish1_thu1, dish2_thu1, dish3_thu1])
    menu_fri1 = Menu(date_fri1, [dish1_fri1, dish2_fri1, dish3_fri1])

    date_mon2 = date(2017, 11, 6)
    date_tue2 = date(2017, 11, 7)
    date_wed2 = date(2017, 11, 8)
    date_thu2 = date(2017, 11, 9)
    date_fri2 = date(2017, 11, 10)
    dish1_mon2 = Dish("Dampfkartoffeln mit Zucchinigemüse", 3.6)
    dish2_mon2 = Dish("Valess-Schnitzel mit Tomaten-Couscous", 4.3)
    dish3_mon2 = Dish("Kasslerpfanne mit frischen Champignons und Spätzle", 4.9)
    dish1_tue2 = Dish("Gemüsereispfanne mit geräuchertem Tofu", 3.6)
    dish2_tue2 = Dish("Schweineschnitzel in Karottenpanade mit Rosmarin- Risoleekartoffeln", 5.3)
    dish1_wed2 = Dish("Spaghetti al Pomodoro", 3.6)
    dish2_wed2 = Dish("Krustenbraten vom Schwein mit Kartoffelknödel und Krautsalat", 5.3)
    dish1_thu2 = Dish("Red-Thaicurrysuppe mit Gemüse und Kokosmilch", 2.9)
    dish2_thu2 = Dish("Senf-Eier mit Salzkartoffeln", 3.8)
    dish3_thu2 = Dish("Putengyros mit Zaziki und Tomatenreis", 5.3)
    dish1_fri2 = Dish("Spiralnudeln mit Ratatouillegemüse", 3.6)
    dish2_fri2 = Dish("Milchreis mit warmen Sauerkirschen", 3)
    dish3_fri2 = Dish("Lasagne aus Seelachs und Blattspinat", 5.3)
    menu_mon2 = Menu(date_mon2, [dish1_mon2, dish2_mon2, dish3_mon2])
    menu_tue2 = Menu(date_tue2, [dish1_tue2, dish2_tue2])
    menu_wed2 = Menu(date_wed2, [dish1_wed2, dish2_wed2])
    menu_thu2 = Menu(date_thu2, [dish1_thu2, dish2_thu2, dish3_thu2])
    menu_fri2 = Menu(date_fri2, [dish1_fri2, dish2_fri2, dish3_fri2])

    def test_Should_Return_Menu(self):
        menus_actual1 = self.bistro_parser.get_menus(self.test_menu1, self.year1, self.week_number1)
        menus_actual2 = self.bistro_parser.get_menus(self.test_menu2, self.year2, self.week_number2)

        self.assertEqual(3, len(menus_actual1))
        self.assertEqual(self.menu_mon1, menus_actual1[self.date_mon1])
        self.assertEqual(self.menu_thu1, menus_actual1[self.date_thu1])
        self.assertEqual(self.menu_fri1, menus_actual1[self.date_fri1])

        self.assertEqual(5, len(menus_actual2))
        self.assertEqual(self.menu_mon2, menus_actual2[self.date_mon2])
        self.assertEqual(self.menu_tue2, menus_actual2[self.date_tue2])
        self.assertEqual(self.menu_wed2, menus_actual2[self.date_wed2])
        self.assertEqual(self.menu_thu2, menus_actual2[self.date_thu2])
        self.assertEqual(self.menu_fri2, menus_actual2[self.date_fri2])


class FMIBistroParserTest(unittest.TestCase):
    ipp_parser = IPPBistroMenuParser()

    def test_Should_Return_Menu(self):
        self.assertEqual(None, self.ipp_parser.get_menus())

