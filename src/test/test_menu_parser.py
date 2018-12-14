# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from lxml import html
from datetime import date

import main
from menu_parser import StudentenwerkMenuParser, FMIBistroMenuParser, IPPBistroMenuParser, MedizinerMensaMenuParser
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
    dish1_1_garching = Dish("Kartoffelgulasch mit Paprika", 1, [])
    dish1_2_garching = Dish("Hackfleischbällchen mit Champignonrahmsauce", 1.9, ["R", "S", "Ei", "Gl", "GlW", "Kn", "Mi"])
    dish1_3_garching = Dish("Seelachsfilet (MSC) im Sesammantel mit Remouladensauce", 2.4, ["1", "2", "3", "9", "Ei", "Fi", "Gl", "GlW", "Mi", "Se", "Sf"])
    dish1_4_garching = Dish("Gebackene Calamari-Ringe mit Remouladensauce", 2.6, ["1", "2", "3", "9", "Ei", "Gl", "GlW", "Mi", "Se", "Sf", "Wt"])

    dish2_1_garching = Dish("Kartoffeleintopf mit Majoran", 1, ["Sl"])
    dish2_2_garching = Dish("Gulasch vom Schwein", 1.9, ["S", "Gl", "GlG", "GlW", "Kn", "Mi"])
    dish2_3_garching = Dish("Paniertes Hähnchenschnitzel", 2.4, ["Gl", "GlW", "GlG", "Kn", "Mi", "Sl"])

    menu1_garching = Menu(menu1_date, [dish1_1_garching, dish1_2_garching, dish1_3_garching, dish1_4_garching])
    menu2_garching = Menu(menu2_date, [dish2_1_garching, dish2_2_garching, dish2_3_garching])

    # dishes in Arcisstrasse
    dish1_1_arcisstrasse = Dish("Kartoffelgulasch mit Paprika", 1, [])
    dish1_2_arcisstrasse = Dish("Hackfleischbällchen mit Champignonrahmsauce", 1.55, ["R", "S", "Ei", "Gl", "GlW", "Kn", "Mi"])
    dish1_3_arcisstrasse = Dish("Hackfleischbällchen mit Champignonrahmsauce (2)", 1.9, ["R", "S", "Ei", "Gl", "GlW", "Kn", "Mi"])
    dish1_4_arcisstrasse = Dish("Pasta Pomodori", 1.9, ["Gl", "GlW", "Kn"])
    dish1_5_arcisstrasse = Dish("Gebackene Calamari-Ringe mit Zitronen-Knoblauch-Dip", 2.6, ["1", "2", "3", "9", "Ei", "Gl", "GlW", "Kn", "Mi", "Sf", "Wt"])
    dish1_6_arcisstrasse = Dish("Seelachsfilet (MSC) im Sesammantel mit Zitronen-Knoblauch-Dip", 2.6, ["1", "3", "9", "Ei", "Fi", "Gl", "GlW", "Kn", "Mi", "Se", "Sf"])
    dish1_7_arcisstrasse = Dish("Pasta Pomodori (2)", "0.68€ / 100g", ["Gl", "GlW", "Kn"])
    dish1_8_arcisstrasse = Dish("Kartoffelgulasch mit Paprika (2)", "0.68€ / 100g", [])
    dish1_9_arcisstrasse = Dish("Pasta mit Sojabolognese", "0.68€ / 100g", ["Sl", "So"])
    menu1_arcisstrasse = Menu(menu1_date, [dish1_1_arcisstrasse, dish1_2_arcisstrasse, dish1_3_arcisstrasse,
                                           dish1_4_arcisstrasse, dish1_5_arcisstrasse, dish1_6_arcisstrasse,
                                           dish1_7_arcisstrasse, dish1_8_arcisstrasse, dish1_9_arcisstrasse])

    # dishes in Großhadern
    dish1_1_großhadern = Dish("Pasta-Gemüse-Auflauf mit Tomatensauce", 1.9, ["1", "Ei", "Gl", "GlW", "Kn", "Mi"])
    dish1_2_großhadern = Dish("Rinderroulade nach Hausfrauenart mit Senf-Gemüse-Sauce", 3, ["R", "S", "2", "3", "99", "Gl", "GlW", "Kn", "Mi", "Sf", "Sl", "Sw"])
    menu1_großhadern = Menu(menu3_date, [dish1_1_großhadern, dish1_2_großhadern])

    def test_Should_ReturnMenu_When_PassedDateIsCorrect(self):
        self.assertEqual(self.menu1_garching,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)[self.menu1_date], "mensa-garching")
        self.assertEqual(self.menu2_garching,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_garching)[self.menu2_date], "mensa-garching")

        self.assertEqual(self.menu1_arcisstrasse,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_arcisstrasse)[self.menu1_date], "mensa-arcisstrasse")

        self.assertEqual(self.menu1_großhadern,
                         self.studentenwerk_menu_parser.get_menus(self.menu_html_großhadern)[self.menu3_date], "stubistro-grosshadern")

    def test_Should_IgnoreDay_When_DateOfTheDayIsInAWrongFormat(self):
        self.assertEqual(22, len(self.studentenwerk_menu_parser.get_menus(self.menu_html_wrong_date_format)), "mensa-garching")

    def test_Should_ReturnWeeks_When_ConvertingMenuToWeekObjects(self):
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching, "mensa-garching")
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

        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching, "mensa-garching")
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
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html_garching, "mensa-garching")
        # get weeks
        weeks = Week.to_weeks(menus)

        # create temp dir for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # store output in the tempdir
            # location can be an empty string because combination won't get tested (combine_dishes is False) here
            main.jsonify(weeks, temp_dir, "", False)

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

    dish_aktion1 = Dish("Tellerfleisch mit Bouillonkartoffeln und Sahnemeerrettich Kaiserschmarrn mit Zwetschenröster",
                        3.0, [])
    dish1_mon1 = Dish("Kurkumareis mit Asia Wokgemüse", 3.6, [])
    dish2_mon1 = Dish("Kartoffel „Cordon Bleu“ mit Frischkäse gefüllt dazu Blattsalate", 4.3, [])
    dish3_mon1 = Dish("Putenschnitzel natur mit Paprikarahmsoße dazu Ebly Gemüseweizen", 5.3, [])
    dish1_thu1 = Dish("Süßkartoffel Gemüsepfanne", 3.6, [])
    dish2_thu1 = Dish("Gemüse Nudelauflauf", 4.3, [])
    dish3_thu1 = Dish("Hähnchenspieß in Kokos Currysoße dazu Früchtereis", 5.3, [])
    dish1_fri1 = Dish("Antipasti Rosmarinkartoffeln", 3.6, [])
    dish2_fri1 = Dish("Schlemmerfilet auf Antipasti Rosmarinkartoffeln", 4.5, [])
    dish3_fri1 = Dish("Kaiserschmarrn mit Zwetschenröster", 3, [])
    menu_mon1 = Menu(date_mon1, [dish_aktion1, dish1_mon1, dish2_mon1, dish3_mon1])
    menu_thu1 = Menu(date_thu1, [dish_aktion1, dish1_thu1, dish2_thu1, dish3_thu1])
    menu_fri1 = Menu(date_fri1, [dish_aktion1, dish1_fri1, dish2_fri1, dish3_fri1])

    date_mon2 = date(2017, 11, 6)
    date_tue2 = date(2017, 11, 7)
    date_wed2 = date(2017, 11, 8)
    date_thu2 = date(2017, 11, 9)
    date_fri2 = date(2017, 11, 10)
    dish_aktion2 = Dish("Pochiertes Lachsfilet mit Dillsoße dazu Minze-Reis", 6.5, [])
    dish1_mon2 = Dish("Dampfkartoffeln mit Zucchinigemüse", 3.6, [])
    dish2_mon2 = Dish("Valess-Schnitzel mit Tomaten-Couscous", 4.3, [])
    dish3_mon2 = Dish("Kasslerpfanne mit frischen Champignons und Spätzle", 4.9, [])
    dish1_tue2 = Dish("Gemüsereispfanne mit geräuchertem Tofu", 3.6, [])
    dish2_tue2 = Dish("Schweineschnitzel in Karottenpanade mit Rosmarin- Risoleekartoffeln", 5.3, [])
    dish1_wed2 = Dish("Spaghetti al Pomodoro", 3.6, [])
    dish2_wed2 = Dish("Krustenbraten vom Schwein mit Kartoffelknödel und Krautsalat", 5.3, [])
    dish1_thu2 = Dish("Red-Thaicurrysuppe mit Gemüse und Kokosmilch", 2.9, [])
    dish2_thu2 = Dish("Senf-Eier mit Salzkartoffeln", 3.8, [])
    dish3_thu2 = Dish("Putengyros mit Zaziki und Tomatenreis", 5.3, [])
    dish1_fri2 = Dish("Spiralnudeln mit Ratatouillegemüse", 3.6, [])
    dish2_fri2 = Dish("Milchreis mit warmen Sauerkirschen", 3, [])
    dish3_fri2 = Dish("Lasagne aus Seelachs und Blattspinat", 5.3, [])
    menu_mon2 = Menu(date_mon2, [dish_aktion2, dish1_mon2, dish2_mon2, dish3_mon2])
    menu_tue2 = Menu(date_tue2, [dish_aktion2, dish1_tue2, dish2_tue2])
    menu_wed2 = Menu(date_wed2, [dish_aktion2, dish1_wed2, dish2_wed2])
    menu_thu2 = Menu(date_thu2, [dish_aktion2, dish1_thu2, dish2_thu2, dish3_thu2])
    menu_fri2 = Menu(date_fri2, [dish_aktion2, dish1_fri2, dish2_fri2, dish3_fri2])

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


class IPPBistroParserTest(unittest.TestCase):
    ipp_parser = IPPBistroMenuParser()
    test_menu1 = open('src/test/assets/ipp/KW-47_20.11-24.11.2017-1.txt', 'r').read()
    year1 = 2017
    week_number1 = 47
    test_menu2 = open('src/test/assets/ipp/KW-48_27.11-01.12.10.2017-3.txt', 'r').read()
    year2 = 2017
    week_number2 = 48

    date_mon1 = date(2017, 11, 20)
    date_tue1 = date(2017, 11, 21)
    date_wed1 = date(2017, 11, 22)
    date_thu1 = date(2017, 11, 23)
    date_fri1 = date(2017, 11, 24)
    dish1_mon1 = Dish("Gefüllter Germknödel mit Vanillesauce", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_mon1 = Dish("Ofengulasch vom Rind mit Kürbis und Pflaumen, dazu Rigatoni", 5.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_mon1 = Dish("\"Palek Tofu\" Gebratener Tofu mit Spinat, Ingwer, Curry-Sahnesauce und Basmatireis", 5.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_mon1 = Dish("Gebratene Hähnchenbrust auf Fenchelgemüse, dazu Kräuterreis und Orangensauce", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_tue1 = Dish("Gebratene Weißkohl-Kartoffelpfanne mit gerösteten Sonnenblumenkernen", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_tue1 = Dish("Jägerschnitzel mit Spätzle oder Reis", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_tue1 = Dish("Vegetarisch gefüllte Tortelli mit leichter Zitronen-Buttersauce und gehobeltem Parmesan", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_tue1 = Dish("\"Bami Goreng\" indonesische Bratnudeln mit Gemüse, Huhn, Schweinefleisch und Pilzen, " \
                      "dazu Honig-Chili- Dip", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_wed1 = Dish("Erbseneintopf (mit Wienerle 4,20 €)", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    # TODO fix "B"
    dish2_wed1 = Dish("Hackbraten mit Zigeunersauce und Reis", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_wed1 = Dish("\"Farfalle Rustico\" mit Champignons, Schinken Tomaten und Peperoni (auf Wunsch mit "
                      "Reibekäse)", 4.6, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_wed1 = Dish("Rumpsteak mit Balsamico Pilzen und Wedges", 7.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_thu1 = Dish("Mediterrane Frittata mit Zucchini, Kartoffeln, Paprika, kleiner Salatbeilage und "
                      "Joghurt-Limetten Dip", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    # TODO fix bug that B of Brett is missing -> rett
    dish2_thu1 = Dish("Frischer Bayrischer Schweinenackenbraten vom Brett geschnitten dazu Kartoffel- Gurkensalat", 4.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_thu1 = Dish("\"Enchilada Verdura\", überbackene Weizentortilla, gefüllt mit Hähnchenfleisch, Sauerrahm, "
                      "Kidneybohnen, Mais, dazu", 5.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_thu1 = Dish("\"Lamm Palak\" mit Spinat und Curry (mittelscharf), dazu Reis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_fri1 = Dish("Nudelpfanne mit Gemüsesauce (auf Wunsch mit Reibekäse)", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_fri1 = Dish("Matjes \"Hausfrauen Art\" mit Salzkartoffeln", 5.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_fri1 = Dish("Currygeschnetzeltes von der Pute mit Früchten und Reis", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_fri1 = Dish("Honig-Kassler mit Apfel-Spitzkohl und Kartoffelspalten", 6.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    menu_mon1 = Menu(date_mon1, [dish1_mon1, dish2_mon1, dish3_mon1, dish4_mon1])
    menu_tue1 = Menu(date_tue1, [dish1_tue1, dish2_tue1, dish3_tue1, dish4_tue1])
    menu_wed1 = Menu(date_wed1, [dish1_wed1, dish2_wed1, dish3_wed1, dish4_wed1])
    menu_thu1 = Menu(date_thu1, [dish1_thu1, dish2_thu1, dish3_thu1, dish4_thu1])
    menu_fri1 = Menu(date_fri1, [dish1_fri1, dish2_fri1, dish3_fri1, dish4_fri1])

    date_mon2 = date(2017, 11, 27)
    date_tue2 = date(2017, 11, 28)
    date_wed2 = date(2017, 11, 29)
    date_thu2 = date(2017, 11, 30)
    date_fri2 = date(2017, 12, 1)
    dish1_mon2 = Dish("Wirsing-Kartoffelauflauf mit Bechamel und Käse", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_mon2 = Dish("Paprikarahm Geschnetzeltes mit Paprikamix und Nudeln", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_mon2 = Dish("\"Dal Curry\" mit Kartoffeln, Kokosmilch, Ingwer, Koriander, Reis und scharfem Chutney", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    # TODO fix missing "R" of "Rinderbraten"
    dish4_mon2 = Dish("Deftiger Hüttenschmaus, Rinderrostbraten mit Zwiebeln, Semmelknödel und gebratenem Gemüse",
                      7.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_tue2 = Dish("Herbstliche Gemüse-Reis Pfanne mit pikantem Mango Dip", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_tue2 = Dish("Krautwickerl mit Speck-Zwieblsauce und Püree", 4.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_tue2 = Dish("Rigatoni mit Rosenkohl und Schnittlauch", 4.6, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_tue2 = Dish("Spanferkelrücken mit Knödel und Bayerisch Kraut", 6.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_wed2 = Dish("Weißwurst Gröst ́l mit Knödel, Lauchzwiebeln, Karotten und Kräuter auf Wunsch mit "
                      "Bratenjus", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_wed2 = Dish("Estragonrahmschnitzel mit Pommes frites oder Reis", 4.6, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_wed2 = Dish("Gemüse Lasagne", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_wed2 = Dish("\"Tandoori Chicken\" mit Auberginen, Tomaten, Zucchini, Zitronenschale Minze und Reis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_thu2 = Dish("Rote Beete Eintopf mit Kartoffeln, Nudeln und Dill", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_thu2 = Dish("Sauerbraten \"Nepal\" mit weißen Bohnen, getrockneten Tomaten und Pasta", 5.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_thu2 = Dish("\"Kaku Chicken\" mit geröstetem Curry, Kokosraspel, Tomaten und Reis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_thu2 = Dish("Leberkäs Burger special mit Pommes frites und Cole slaw", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish1_fri2 = Dish("Exotische Linsen-Spätzle Pfanne", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish2_fri2 = Dish("Seelachsfilet gebacken mit Sardellenmayonnaise und Pommes frites", 4.6, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish3_fri2 = Dish("Gemüse-Linguini mit Pesto-Rahmsauce und Parmesankäse", 4.4, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    dish4_fri2 = Dish("Schweinefilet Medaillons in grüner Pfefferrahmsauce mit Kroketten und karamellisierten "
                      "Möhren", 7.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])

    menu_mon2 = Menu(date_mon2, [dish1_mon2, dish2_mon2, dish3_mon2, dish4_mon2])
    menu_tue2 = Menu(date_tue2, [dish1_tue2, dish2_tue2, dish3_tue2, dish4_tue2])
    menu_wed2 = Menu(date_wed2, [dish1_wed2, dish2_wed2, dish3_wed2, dish4_wed2])
    menu_thu2 = Menu(date_thu2, [dish1_thu2, dish2_thu2, dish3_thu2, dish4_thu2])
    menu_fri2 = Menu(date_fri2, [dish1_fri2, dish2_fri2, dish3_fri2, dish4_fri2])

    def test_Should_Return_Menu1(self):
        menus_actual1 = self.ipp_parser.get_menus(self.test_menu1, self.year1, self.week_number1)
        self.assertEqual(5, len(menus_actual1))
        self.assertEqual(self.menu_mon1, menus_actual1[self.date_mon1])
        self.assertEqual(self.menu_tue1, menus_actual1[self.date_tue1])
        self.assertEqual(self.menu_wed1, menus_actual1[self.date_wed1])
        self.assertEqual(self.menu_thu1, menus_actual1[self.date_thu1])
        self.assertEqual(self.menu_fri1, menus_actual1[self.date_fri1])

    def test_Should_Return_Menu2(self):
        menus_actual2 = self.ipp_parser.get_menus(self.test_menu2, self.year2, self.week_number2)
        self.assertEqual(5, len(menus_actual2))
        self.assertEqual(self.menu_mon2, menus_actual2[self.date_mon2])
        self.assertEqual(self.menu_tue2, menus_actual2[self.date_tue2])
        self.assertEqual(self.menu_wed2, menus_actual2[self.date_wed2])
        self.assertEqual(self.menu_thu2, menus_actual2[self.date_thu2])
        self.assertEqual(self.menu_fri2, menus_actual2[self.date_fri2])

    ## Test Cases with holidays

    ## Two holidays (Mon & Tue)

    y18w18_date_mon = date(2018, 4, 30)
    y18w18_date_tue = date(2018, 5, 1)
    y18w18_date_wed = date(2018, 5, 2)
    y18w18_date_thu = date(2018, 5, 3)
    y18w18_date_fri = date(2018, 5, 4)

    y18w18_dishes_wed = [
        Dish("Kirschmichel mit Vanillesauce", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Fitnessteak vom Grill, dazu Zitrone oder Kräuterbutter, Grilltomate und Ofenkartoffel mit "
             "Sauerrahmdip oder bunter Salatauswahl", 8.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("\"Chana Dal\" Kichererbsen, Kartoffeln, Kokosmilch, Curryblätter und Reis", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Calamari alla Romana, gebackene Tintenfischringe mit Knoblauchmayonnaise und "
             "gemischtem Blattsalat mit Tomate und Gurke", 6.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])
    ]

    y18w18_dishes_thu = [
        Dish("Grenaillekartoffeln mit Apfel-Möhren-Quark, auf Wunsch mit gerösteten Sonnenblumenkernen", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Böfflamott, gebeizter Rinderschmorbraten mit Rotwein, dazu Frühlingsgemüse und Semmelknödel", 6.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Fussili mit Lauch, Ricotta, Meerrettich und frischem Basilikum", 4.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Aus dem Wok Putengeschnetzeltes mit Mangold, Möhren, Frühlings- zwiebeln und Basmatireis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w18_dishes_fri = [
        Dish("Curryreispfanne mit Gemüse, Ananas, Kreuzkümmel, Koriander und Chili-Dip", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Zitronen Seelachs auf Paprika-Champignon Gemüse, Petersilien- Kartoffeln und leichter Buttersauce", 5.90, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Paprikarahmgeschnetzeltes mit Hörnchennudeln", 5.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("\"Pasta Arora\" italienische Nudeln mit Tomatensahne, Mozzarella und Basilikum", 4.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w18_menu_mon = Menu(y18w18_date_mon, [])
    y18w18_menu_tue = Menu(y18w18_date_tue, [])
    y18w18_menu_wed = Menu(y18w18_date_wed, y18w18_dishes_wed)
    y18w18_menu_thu = Menu(y18w18_date_thu, y18w18_dishes_thu)
    y18w18_menu_fri = Menu(y18w18_date_fri, y18w18_dishes_fri)

    y18w18_test_menu = open('src/test/assets/ipp/KW-18_30.04.-04.05.18.txt', 'r').read()

    def test_Holiday_Should_Return_Menu_y18w18(self):
        menus_actual = self.ipp_parser.get_menus(self.y18w18_test_menu, year=2018, week_number=18)
        self.assertEqual(5, len(menus_actual))

        self.assertEqual(self.y18w18_menu_mon, menus_actual[self.y18w18_date_mon])
        self.assertEqual(self.y18w18_menu_tue, menus_actual[self.y18w18_date_tue])
        self.assertEqual(self.y18w18_menu_wed, menus_actual[self.y18w18_date_wed])
        self.assertEqual(self.y18w18_menu_thu, menus_actual[self.y18w18_date_thu])
        self.assertEqual(self.y18w18_menu_fri, menus_actual[self.y18w18_date_fri])

    ## One holiday (Thu)

    y18w19_date_mon = date(2018, 5, 7)
    y18w19_date_tue = date(2018, 5, 8)
    y18w19_date_wed = date(2018, 5, 9)
    y18w19_date_thu = date(2018, 5, 10)
    y18w19_date_fri = date(2018, 5, 11)

    y18w19_dishes_mon = [
        Dish("Gemüse-Schupfnudeln dazu Sauerrahm-Dip", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Würziger Putenbrustbraten mit Frühlingsgemüse und Kroketten", 7.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Gnocchi-Lauch Gratin mit Käse überbacken", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Schweinefleisch süß-sauer mit Ananas, Paprika, Tomaten und Reis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w19_dishes_tue = [
        Dish("Gebackener Edamer mit Rohkostsalat und Preiselbeeren", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Köttbullar (Hackfleischbällchen) mit Rahmsauce, Preiselbeeren und Petersilienkartoffeln", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Burgunderbraten vom Rind mit Knödel und Blaukraut", 6.2, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Quarkknödel auf Erdbeer-Rhabarber Kompott", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w19_dishes_wed = [
        Dish("Italienische Minestrone mit Reis", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Gebackenes Schweineschnitzel mit Zitrone und Pommes frites", 5.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("\"Vegetarian Vindaloo\" Kartoffeln und Tomaten in Currysauce, dazu Reis und frischer Koriander", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        # Note the " after the Basilikum is correct since it is part of the PDF
        Dish("Farfalle \"al Tonno\" mit Thunfisch, Kapern, Oliven, Tomaten und Basilikum\"", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w19_dishes_fri = [
        Dish("Spaghetti mit Tomatensauce und Reibekäse", 3.5, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("2 Paar Schweinswürst ́l auf Sauerkraut und Püree", 4.8, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("\"Chicken Padam Pasanda\" mit Nusssauce, Kokos- flocken und indischen Gewürzen, dazu Basmatireis", 6.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"]),
        Dish("Kartoffeltasche, gefüllt mit Kräuterfrischkäse auf Paprikagemüse", 4.9, ["Mi", "Gl", "Sf", "Sl", "Ei", "Se", "4"])]

    y18w19_menu_mon = Menu(y18w19_date_mon, y18w19_dishes_mon)
    y18w19_menu_tue = Menu(y18w19_date_tue, y18w19_dishes_tue)
    y18w19_menu_wed = Menu(y18w19_date_wed, y18w19_dishes_wed)
    y18w19_menu_thu = Menu(y18w19_date_thu, [])
    y18w19_menu_fri = Menu(y18w19_date_fri, y18w19_dishes_fri)

    y18w19_test_menu = open('src/test/assets/ipp/KW-19_07.05.-11.05.18.txt', 'r').read()

    def test_Holiday_Should_Return_Menu_y18w19(self):
        menus_actual = self.ipp_parser.get_menus(self.y18w19_test_menu, year=2018, week_number=19)
        self.assertEqual(5, len(menus_actual))

        self.assertEqual(self.y18w19_menu_mon, menus_actual[self.y18w19_date_mon])
        self.assertEqual(self.y18w19_menu_tue, menus_actual[self.y18w19_date_tue])
        self.assertEqual(self.y18w19_menu_wed, menus_actual[self.y18w19_date_wed])
        self.assertEqual(self.y18w19_menu_thu, menus_actual[self.y18w19_date_thu])
        self.assertEqual(self.y18w19_menu_fri, menus_actual[self.y18w19_date_fri])


class MedizinerMensaParserTest(unittest.TestCase):
    mediziner_mensa_parser = MedizinerMensaMenuParser()
    test_menu1 = open('src/test/assets/mediziner-mensa/KW_44_Herbst_4_Mensa_2018.txt', 'r').read()
    year1 = 2018
    week_number1 = 44

    date_mon1 = date(2018, 10, 29)
    date_tue1 = date(2018, 10, 30)
    date_wed1 = date(2018, 10, 31)
    date_thu1 = date(2018, 11, 1)
    date_fri1 = date(2018, 11, 2)
    date_sat1 = date(2018, 11, 3)
    date_sun1 = date(2018, 11, 4)

    dish1_mon1 = Dish("Spinatcremesuppe", "N/A", [])
    dish2_mon1 = Dish("Gekochtes Ochsenfleisch mit Meerrettich", "N/A", [])
    dish3_mon1 = Dish("Kürbisauflauf", "N/A", [])
    dish4_mon1 = Dish("Asiatische Gemüse-Puten-Pfanne mit Reisnudeln", "N/A", [])

    dish1_tue1 = Dish("Selleriecremesuppe", "N/A", [])
    dish2_tue1 = Dish("Oldenburger Grünkohl mit Mettenden", "N/A", [])
    dish3_tue1 = Dish("Kaschmir Kohlrabi und Brokkoli", "N/A", [])
    dish4_tue1 = Dish("Conchiglioni Nudeln mit mit mediterranem Gemüse", "N/A", [])

    dish1_wed1 = Dish("Französische Zwiebelsuppe", "N/A", [])
    dish2_wed1 = Dish("Germknödel mit Vanillesoße", "N/A", [])
    dish3_wed1 = Dish("Herzhaftes Kartoffelgratin", "N/A", [])
    dish4_wed1 = Dish("Holzfällersteak mit Bratkartoffeln und Weißkrautsalat", "N/A", [])

    dish1_thu1 = Dish("Süßkartoffelcremesuppe", "N/A", [])
    dish2_thu1 = Dish("Hähnchenbrust gegrillt", "N/A", [])
    dish3_thu1 = Dish("In Sesamöl gebratenes Wokgemüse", "N/A", [])

    dish1_fri1 = Dish("Brokkolicremesuppe", "N/A", [])
    dish2_fri1 = Dish("Forelle \"Müllerin Art \"", "N/A", [])
    dish3_fri1 = Dish("Quarkklößchen", "N/A", [])
    dish4_fri1 = Dish("Chili con Cous Cous mit Kürbis-Apfel-Salat", "N/A", [])

    dish1_sat1 = Dish("Bratspätzlesuppe", "N/A", [])
    dish2_sat1 = Dish("Geflügelpflanzerl", "N/A", [])
    dish3_sat1 = Dish("Krauttopf mit einer Vollkornsemmel", "N/A", [])

    dish1_sun1 = Dish("Käsecremesuppe", "N/A", [])
    dish2_sun1 = Dish("Geschmortes Kalbfleisch", "N/A", [])
    dish3_sun1 = Dish("Vegetarische Moussaka", "N/A", [])

    menu_mon1 = Menu(date_mon1, [dish1_mon1, dish2_mon1, dish3_mon1, dish4_mon1])
    menu_tue1 = Menu(date_tue1, [dish1_tue1, dish2_tue1, dish3_tue1, dish4_tue1])
    menu_wed1 = Menu(date_wed1, [dish1_wed1, dish2_wed1, dish3_wed1, dish4_wed1])
    menu_thu1 = Menu(date_thu1, [dish1_thu1, dish2_thu1, dish3_thu1])
    menu_fri1 = Menu(date_fri1, [dish1_fri1, dish2_fri1, dish3_fri1, dish4_fri1])
    menu_sat1 = Menu(date_sat1, [dish1_sat1, dish2_sat1, dish3_sat1])
    menu_sun1 = Menu(date_sun1, [dish1_sun1, dish2_sun1, dish3_sun1])

    test_menu2 = open('src/test/assets/mediziner-mensa/KW_47_Herbst_3_Mensa_2018.txt', 'r').read()
    year2 = 2018
    week_number2 = 47

    date_mon2 = date(2018, 11, 19)
    date_tue2 = date(2018, 11, 20)
    date_wed2 = date(2018, 11, 21)
    date_thu2 = date(2018, 11, 22)
    date_fri2 = date(2018, 11, 23)
    date_sat2 = date(2018, 11, 24)
    date_sun2 = date(2018, 11, 25)

    dish1_mon2 = Dish("Blumenkohlcremesuppe", "N/A", [])
    dish2_mon2 = Dish("Pfannengyros mit Tzaziki", "N/A", [])
    dish3_mon2 = Dish("Spaghetti \" Gemüsebolognese \"", "N/A", [])
    dish4_mon2 = Dish("Thai-Curry aus Blumenkohl und Kartoffeln mit Gemüsreis und Salat", "N/A", [])

    dish1_tue2 = Dish("Gelbe Erbsensuppe", "N/A", [])
    dish2_tue2 = Dish("Grüner Bohneneintopf mit Rindfleisch", "N/A", [])
    dish3_tue2 = Dish("Veggi-Gulasch", "N/A", [])
    dish4_tue2 = Dish("Rotbarschfischfilet in Dillsoße mit Kürbisgemüse und Wacholderreis", "N/A", [])

    dish1_wed2 = Dish("Rinderbrühe \" Gärtnerin \"", "N/A", [])
    dish2_wed2 = Dish("Schweinegulasch", "N/A", [])
    dish3_wed2 = Dish("Gemüsekuchen mit Mozzarella überbacken", "N/A", [])
    dish4_wed2 = Dish("Schinkennudeln mit Tomatensoße, dazu gemischter Salat", "N/A", [])

    dish1_thu2 = Dish("Kürbiscremesuppe", "N/A", [])
    dish2_thu2 = Dish("Rinderhackbraten", "N/A", [])
    dish3_thu2 = Dish("Dinkel-Kräuterbratling", "N/A", [])
    dish4_thu2 = Dish("Pikantes Risotto mit buntem Gemüse und Tomatensalat mit Basilikum", "N/A", [])

    dish1_fri2 = Dish("Minestrone", "N/A", [])
    dish2_fri2 = Dish("Gebratene Hähnchenbrust", "N/A", [])
    dish3_fri2 = Dish("Scheiterhaufen  mit Apfel-Vanille-Ragout", "N/A", [])
    dish4_fri2 = Dish("Paniertes Schnitzel vom Schwein und Pute mit Kartoffelmayosalat und Zitronenecke", "N/A", [])

    dish1_sat2 = Dish("Tomatencremesuppe", "N/A", [])
    dish2_sat2 = Dish("Pichelsteiner Gemüseeintopf mit Rindfleisch", "N/A", [])
    dish3_sat2 = Dish("Ofenkartoffel mit herzhaftem Gemüseragout", "N/A", [])

    dish1_sun2 = Dish("Grießnockerlsuppe", "N/A", [])
    dish2_sun2 = Dish("Glasierter Putenbraten in Kräuterrahmsoße", "N/A", [])
    dish3_sun2 = Dish("Eieromelett", "N/A", [])

    menu_mon2 = Menu(date_mon2, [dish1_mon2, dish2_mon2, dish3_mon2, dish4_mon2])
    menu_tue2 = Menu(date_tue2, [dish1_tue2, dish2_tue2, dish3_tue2, dish4_tue2])
    menu_wed2 = Menu(date_wed2, [dish1_wed2, dish2_wed2, dish3_wed2, dish4_wed2])
    menu_thu2 = Menu(date_thu2, [dish1_thu2, dish2_thu2, dish3_thu2, dish4_thu2])
    menu_fri2 = Menu(date_fri2, [dish1_fri2, dish2_fri2, dish3_fri2, dish4_fri2])
    menu_sat2 = Menu(date_sat2, [dish1_sat2, dish2_sat2, dish3_sat2])
    menu_sun2 = Menu(date_sun2, [dish1_sun2, dish2_sun2, dish3_sun2])

    def test_Should_Return_Menu1(self):
        menus_actual1 = self.mediziner_mensa_parser.get_menus(self.test_menu1, self.year1, self.week_number1)
        self.assertEqual(7, len(menus_actual1))
        self.assertEqual(self.menu_mon1, menus_actual1[self.date_mon1])
        self.assertEqual(self.menu_tue1, menus_actual1[self.date_tue1])
        self.assertEqual(self.menu_wed1, menus_actual1[self.date_wed1])
        self.assertEqual(self.menu_thu1, menus_actual1[self.date_thu1])
        self.assertEqual(self.menu_fri1, menus_actual1[self.date_fri1])
        self.assertEqual(self.menu_sat1, menus_actual1[self.date_sat1])
        self.assertEqual(self.menu_sun1, menus_actual1[self.date_sun1])

        menus_actual2 = self.mediziner_mensa_parser.get_menus(self.test_menu2, self.year2, self.week_number2)
        self.assertEqual(7, len(menus_actual2))
        self.assertEqual(self.menu_mon2, menus_actual2[self.date_mon2])
        self.assertEqual(self.menu_tue2, menus_actual2[self.date_tue2])
        self.assertEqual(self.menu_wed2, menus_actual2[self.date_wed2])
        self.assertEqual(self.menu_thu2, menus_actual2[self.date_thu2])
        self.assertEqual(self.menu_fri2, menus_actual2[self.date_fri2])
        self.assertEqual(self.menu_sat2, menus_actual2[self.date_sat2])
        self.assertEqual(self.menu_sun2, menus_actual2[self.date_sun2])
