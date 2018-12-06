# -*- coding: utf-8 -*-

import re
import sys
import tempfile
import unicodedata
from datetime import datetime
from subprocess import call
from warnings import warn

import requests
from lxml import html

import util
from entities import Dish, Menu, Ingredients


class MenuParser:
    weekday_positions = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 0}

    def get_date(self, year, week_number, day):
        # get date from year, week number and current weekday
        # https://stackoverflow.com/questions/17087314/get-date-from-week-number
        date_str = "%d-W%d-%d" % (year, week_number, day)
        date = datetime.strptime(date_str, "%Y-W%W-%w").date()
        return date

    def parse(self, location):
        pass


class StudentenwerkMenuParser(MenuParser):
    prices = {
        "Tagesgericht 1": 1, "Tagesgericht 2": 1.55, "Tagesgericht 3": 1.9, "Tagesgericht 4": 2.4,
        "Aktionsessen 1": 1.55, "Aktionsessen 2": 1.9, "Aktionsessen 3": 2.4, "Aktionsessen 4": 2.6,
        "Aktionsessen 5": 2.8, "Aktionsessen 6": 3.0, "Aktionsessen 7": 3.2, "Aktionsessen 8": 3.5, "Aktionsessen 9": 4,
        "Aktionsessen 10": 4.5, "Biogericht 1": 1.55, "Biogericht 2": 1.9, "Biogericht 3": 2.4, "Biogericht 4": 2.6,
        "Biogericht 5": 2.8, "Biogericht 6": 3.0, "Biogericht 7": 3.2, "Biogericht 8": 3.5, "Biogericht 9": 4,
        "Biogericht 10": 4.5, "Self-Service": "0.68€ / 100g", "Self-Service Arcisstraße": "0.68€ / 100g",
        "Self-Service Grüne Mensa": "0.33€ / 100g", "Baustellenteller": "Baustellenteller (> 2.40€)",
        "Fast Lane": "Fast Lane (> 3.50€)", "Länder-Mensa": "0.75€ / 100g", "Mensa Spezial Pasta": "0.60€ / 100g",
        "Mensa Spezial": "individual",  # 0.85€ / 100g (one-course dishes have individual prices)
    }

    # Some of the locations do not use the general Studentenwerk system and do not have a location id.
    # It differs how they publish their menus — probably everyone needs an own parser.
    # For documentation they are in the list but commented out.
    location_id_mapping = {
        "mensa-arcisstr": 421,
        "mensa-arcisstrasse": 421,  # backwards compatibility
        "mensa-garching": 422,
        "mensa-leopoldstr": 411,
        "mensa-lothstr": 431,
        "mensa-martinsried": 412,
        "mensa-pasing": 432,
        "mensa-weihenstephan": 423,
        "stubistro-arcisstr": 450,
        # "stubistro-benediktbeuern": ,
        "stubistro-goethestr": 418,
        "stubistro-großhadern": 414,
        "stubistro-grosshadern": 414,
        "stubistro-rosenheim": 441,
        "stubistro-schellingstr": 416,
        # "stubistro-schillerstr": ,
        "stucafe-adalbertstr": 512,
        "stucafe-akademie-weihenstephan": 526,
        # "stucafe-audimax" ,
        "stucafe-boltzmannstr": 527,
        "stucafe-garching": 524,
        # "stucafe-heßstr": ,
        "stucafe-karlstr": 532,
        # "stucafe-leopoldstr": ,
        # "stucafe-olympiapark": ,
        "stucafe-pasing": 534,
        # "stucafe-weihenstephan": ,
    }

    base_url = "http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_{}_-de.html"

    def parse(self, location):
        """`location` can be either the numeric location id or its string alias as defined in `location_id_mapping`"""
        try:
            location_id = int(location)
        except ValueError:
            try:
                location_id = self.location_id_mapping[location]
            except KeyError:
                print("Location {} not found. Choose one of {}.".format(
                    location, ', '.join(self.location_id_mapping.keys())), sys.stderr)
                return None

        page_link = self.base_url.format(location_id)

        page = requests.get(page_link)
        tree = html.fromstring(page.content)
        return self.get_menus(tree, location)

    def get_menus(self, page, location):
        # initialize empty dictionary
        menus = {}
        # convert passed date to string
        # get all available daily menus
        daily_menus = self.__get_daily_menus_as_html(page)

        # iterate through daily menus
        for daily_menu in daily_menus:
            # get html representation of current menu
            menu_html = html.fromstring(html.tostring(daily_menu))
            # get the date of the current menu; some string modifications are necessary
            current_menu_date_str = menu_html.xpath("//strong/text()")[0]
            # parse date
            try:
                current_menu_date = util.parse_date(current_menu_date_str)
            except ValueError as e:
                print("Warning: Error during parsing date from html page. Problematic date: %s" % current_menu_date_str)
                # continue and parse subsequent menus
                continue
            # parse dishes of current menu
            dishes = self.__parse_dishes(menu_html, location)
            # create menu object
            menu = Menu(current_menu_date, dishes)
            # add menu object to dictionary using the date as key
            menus[current_menu_date] = menu

        # return the menu for the requested date; if no menu exists, None is returned
        return menus

    @staticmethod
    def __get_daily_menus_as_html(page):
        # obtain all daily menus found in the passed html page by xpath query
        daily_menus = page.xpath("//div[@class='c-schedule__item']")
        return daily_menus

    @staticmethod
    def __parse_dishes(menu_html, location):
        # obtain the names of all dishes in a passed menu
        dish_names = [dish.rstrip() for dish in menu_html.xpath("//p[@class='js-schedule-dish-description']/text()")]
        # make duplicates unique by adding (2), (3) etc. to the names
        dish_names = util.make_duplicates_unique(dish_names)
        # obtain the types of the dishes (e.g. 'Tagesgericht 1')
        dish_types = [type.text if type.text else '' for type in menu_html.xpath("//span[@class='stwm-artname']")]
        # obtain all ingredients
        dish_markers_additional = menu_html.xpath("//span[contains(@class, 'c-schedule__marker--additional')]/@data-essen")
        dish_markers_allergen = menu_html.xpath("//span[contains(@class, 'c-schedule__marker--allergen')]/@data-essen")

        # create dictionary out of dish name and dish type
        dishes_dict = {}
        dishes_tup = zip(dish_names, dish_types, dish_markers_additional, dish_markers_allergen)
        for dish_name, dish_type, dish_marker_additional, dish_marker_allergen in dishes_tup:
            dishes_dict[dish_name] = (dish_type, dish_marker_additional, dish_marker_allergen)

        # create Dish objects with correct prices; if price is not available, -1 is used instead
        dishes = []
        for name in dishes_dict:
            if not dishes_dict[name] and dishes:
                # some dishes are multi-row. That means that for the same type the dish is written in multiple rows.
                # From the second row on the type is then just empty. In that case, we just use the price and
                # ingredients of the previous dish.
                dishes.append(Dish(name, dishes[-1].price, dishes[-1].ingredients))
            else:
                dish_ingredients = Ingredients(location)
                dish_ingredients.parse_ingredients(dishes_dict[name][1])
                dish_ingredients.parse_ingredients(dishes_dict[name][2])
                dishes.append(Dish(name, StudentenwerkMenuParser.prices.get(dishes_dict[name][0], "N/A"), dish_ingredients.ingredient_list))

        return dishes


class FMIBistroMenuParser(MenuParser):
    url = "http://www.wilhelm-gastronomie.de/tum-garching"
    allergens = ["Gluten", "Laktose", "Milcheiweiß", "Hühnerei", "Soja", "Nüsse", "Erdnuss", "Sellerie", "Fisch",
                 "Krebstiere", "Weichtiere", "Sesam", "Senf", "Milch", "Ei"]
    price_regex = r"\€\s\d+,\d+"
    dish_regex = r".+?\€\s\d+,\d+"

    def parse(self, location):
        # get web page of bistro
        page = requests.get(self.url)
        # get html tree
        tree = html.fromstring(page.content)
        # get url of current pdf menu
        xpath_query = tree.xpath("//a[contains(@href, 'Speiseplan')]/@href")

        if len(xpath_query) < 1:
            return None

        menus = {}
        for pdf_url in xpath_query:
            # Example PDF-name: Garching-Speiseplan_KW46_2017.pdf
            # more examples: https://regex101.com/r/ATOHj3/3
            pdf_name = pdf_url.split("/")[-1]
            wn_year_match = re.search("KW[^a-zA-Z1-9]*([1-9]+\d*)[^a-zA-Z1-9]*([1-9]+\d{3})?", pdf_name, re.IGNORECASE)
            week_number = int(wn_year_match.group(1)) if wn_year_match else None
            year = int(wn_year_match.group(2)) if wn_year_match and wn_year_match.group(2) else None

            today = datetime.today()
            # a hacky way to detect when something is appended or prepended to the year (like 20181 for year 2018)
            # TODO probably replace year abnormality by a better method
            if (year != today.year and str(today.year) in str(year)) or year is None:
                year = today.year

            with tempfile.NamedTemporaryFile() as temp_pdf:
                # download pdf
                response = requests.get(pdf_url)
                temp_pdf.write(response.content)
                with tempfile.NamedTemporaryFile() as temp_txt:
                    # convert pdf to text by calling pdftotext
                    call(["pdftotext", "-layout", temp_pdf.name, temp_txt.name])
                    with open(temp_txt.name, 'r') as myfile:
                        # read generated text file
                        data = myfile.read()
                        parsed_menus = self.get_menus(data, year, week_number)
                        if parsed_menus is not None:
                            menus.update(parsed_menus)

        return menus

    def get_menus(self, text, year, week_number):
        menus = {}
        lines = text.splitlines()
        count = 0
        # remove headline etc.
        for line in lines:
            if line.replace(" ", "").replace("\n", "").lower() == "montagdienstagmittwochdonnerstagfreitag":
                break

            count += 1

        lines = lines[count:]
        # we assume that the weeksdays are now all in the first line
        pos_mon = lines[0].find("Montag")
        pos_tue = lines[0].find("Dienstag")
        pos_wed = lines[0].find("Mittwoch")
        pos_thu = lines[0].find("Donnerstag")
        pos_fri = lines[0].find("Freitag")

        # The text is formatted as table using whitespaces. Hence, we need to get those parts of each line that refer
        #  to the respective week day
        lines_weekdays = {"mon": "", "tue": "", "wed": "", "thu": "", "fri": ""}
        for line in lines:
            lines_weekdays["mon"] += " " + line[pos_mon:pos_tue].replace("\n", " ").replace("Montag", "")
            lines_weekdays["tue"] += " " + line[pos_tue:pos_wed].replace("\n", " ").replace("Dienstag", "")
            lines_weekdays["wed"] += " " + line[pos_wed:pos_thu].replace("\n", " ").replace("Mittwoch", "")
            lines_weekdays["thu"] += " " + line[pos_thu:pos_fri].replace("\n", " ").replace("Donnerstag", "")
            lines_weekdays["fri"] += " " + line[pos_fri:].replace("\n", " ").replace("Freitag", "")

        # currently, up to 5 dishes are on the menu
        num_dishes = 5
        line_aktion = []
        if year < 2018:
            # in older versions of the FMI Bistro menu, the Aktionsgericht was the same for the whole week
            num_dishes = 3
            line_aktion = [s for s in lines if "Aktion" in s]
            if len(line_aktion) == 1:
                line_aktion_pos = lines.index(line_aktion[0]) - 2
                aktionsgericht = ' '.join(lines[line_aktion_pos:line_aktion_pos + 3])
                aktionsgericht = aktionsgericht \
                    .replace("Montag – Freitag", "") \
                    .replace("Tagessuppe täglich wechselndes Angebot", "") \
                    .replace("ab € 1,00", "") \
                    .replace("Aktion", "")
                num_dishes += aktionsgericht.count('€')
                for key in lines_weekdays:
                    lines_weekdays[key] = aktionsgericht + ", " + lines_weekdays[key]

        # Process menus for each day
        for key in lines_weekdays:
            # stop parsing day when bistro is closed at that day
            if "geschlossen" in lines_weekdays[key].lower():
                continue

            lines_weekdays[key] = lines_weekdays[key].replace("Allergene:", "")
            # get rid of two-character umlauts (e.g. SMALL_LETTER_A+COMBINING_DIACRITICAL_MARK_UMLAUT)
            lines_weekdays[key] = unicodedata.normalize("NFKC", lines_weekdays[key])
            # remove multi-whitespaces
            lines_weekdays[key] = ' '.join(lines_weekdays[key].split())
            # remove allergnes
            for allergen in self.allergens:
                # only replace "whole word matches" not followed by a hyphen (e.g. some dishes include "Senf-")
                lines_weekdays[key] = re.sub(r"\b%s\b(?![\w-])" % allergen, "", lines_weekdays[key])

            # remove no allergenes indicator
            lines_weekdays[key] = lines_weekdays[key].replace("./.", "")
            # get all dish including name and price
            dish_names = re.findall(self.dish_regex, lines_weekdays[key])
            # get dish prices
            prices = re.findall(self.price_regex, ' '.join(dish_names))
            # convert prices to float
            prices = [float(price.replace("€", "").replace(",", ".").strip()) for price in prices]
            # remove price and commas from dish names
            dish_names = [re.sub(self.price_regex, "", dish).replace(",", "").strip() for dish in dish_names]
            # create list of Dish objects; only take first 3/4 as the following dishes are corrupt and not necessary
            dishes = [Dish(dish_name, price) for (dish_name, price) in list(zip(dish_names, prices), Ingredients("fmi-bistro"))][:num_dishes]
            # filter empty dishes
            dishes = list(filter(lambda x: x.name != "", dishes))
            date = self.get_date(year, week_number, self.weekday_positions[key])
            # create new Menu object and add it to dict
            menu = Menu(date, dishes)
            # remove duplicates
            menu.remove_duplicates()
            menus[date] = menu

        return menus


class IPPBistroMenuParser(MenuParser):
    url = "http://konradhof-catering.de/ipp/"
    split_days_regex = re.compile('(Tagessuppe siehe Aushang|Aushang|Aschermittwoch|Feiertag|Geschlossen)',
                                  re.IGNORECASE)
    split_days_regex_soup_one_line = re.compile('T agessuppe siehe Aushang|Tagessuppe siehe Aushang', re.IGNORECASE)
    split_days_regex_soup_two_line = re.compile('Aushang', re.IGNORECASE)
    split_days_regex_closed = re.compile('Aschermittwoch|Feiertag|Geschlossen', re.IGNORECASE)
    price_regex = re.compile("\d+,\d+\s\€[^\)]")
    dish_regex = re.compile(".+?\d+,\d+\s\€[^\)]")

    def parse(self, location):
        page = requests.get(self.url)
        # get html tree
        tree = html.fromstring(page.content)
        # get url of current pdf menu
        xpath_query = tree.xpath("//a[contains(@title, 'KW-')]/@href")

        if len(xpath_query) < 1:
            return None

        menus = {}
        for pdf_url in xpath_query:
            # Example PDF-name: KW-48_27.11-01.12.10.2017-3.pdf
            pdf_name = pdf_url.split("/")[-1]
            # more examples: https://regex101.com/r/hwdpFx/1
            wn_year_match = re.search("KW[^a-zA-Z1-9]*([1-9]+\d*).*\d+\.\d+\.(\d+).*", pdf_name, re.IGNORECASE)
            week_number = int(wn_year_match.group(1)) if wn_year_match else None
            year = int(wn_year_match.group(2)) if wn_year_match else None
            # convert 2-digit year into 4-digit year
            year = 2000 + year if year is not None and len(str(year)) == 2 else year

            with tempfile.NamedTemporaryFile() as temp_pdf:
                # download pdf
                response = requests.get(pdf_url)
                temp_pdf.write(response.content)
                with tempfile.NamedTemporaryFile() as temp_txt:
                    # convert pdf to text by calling pdftotext; only convert first page to txt (-l 1)
                    call(["pdftotext", "-l", "1", "-layout", temp_pdf.name, temp_txt.name])
                    with open(temp_txt.name, 'r') as myfile:
                        # read generated text file
                        data = myfile.read()
                        parsed_menus = self.get_menus(data, year, week_number)
                        if parsed_menus is not None:
                            menus.update(parsed_menus)

        return menus

    def get_menus(self, text, year, week_number):
        menus = {}
        lines = text.splitlines()
        count = 0
        # remove headline etc.
        for line in lines:
            if line.replace(" ", "").replace("\n", "").lower() == "montagdienstagmittwochdonnerstagfreitag":
                break

            count += 1

        lines = lines[count:]
        weekdays = lines[0]

        # The column detection is done through the string "Tagessuppe siehe Aushang" which is at the beginning of
        # every column. However, due to center alignment the column do not begin at the 'T' character and broader
        # text in the column might be left of this character, which then gets truncated. But the gap between the 'T'
        # and the '€' character of the previous column¹ — the real beginning of the current column — is always three,
        # which will be subtracted here. Monday is the second column, so the value should never become negative
        # although it is handled here.
        # ¹or 'e' of "Internationale Küche" if it is the monday column

        # find lines which match the regex
        soup_lines_iter = (x for x in lines if self.split_days_regex.search(x))

        soup_line1 = next(soup_lines_iter)
        soup_line2 = next(soup_lines_iter, '')

        positions1 = [(max(a.start() - 3, 0), a.end()) for a in list(
            re.finditer(self.split_days_regex_soup_one_line, soup_line1))]
        # In the second line there is just 'Aushang' (two lines "Tagessuppe siehe Aushang" or
        # closed days ("Geschlossen", "Feiertag")
        positions2 = [(max(a.start() - 14, 0), a.end() + 3) for a in list(
            re.finditer(self.split_days_regex_soup_two_line, soup_line2))]
        positions3 = [(max(a.start() - 3, 0), a.end()) for a in list(
            re.finditer(self.split_days_regex_closed, soup_line2))]

        if positions2: # Two lines "Tagessuppe siehe Aushang"
            soup_line_index = lines.index(soup_line2)
        else:
            soup_line_index = lines.index(soup_line1)

        positions = sorted(positions1 + positions2 + positions3)

        if len(positions) != 5:
            warn("IPP PDF parsing of week {} in year {} failed. Only {} of 5 columns detected.".format(
                week_number, year, len(positions)))
            return None

        pos_mon = positions[0][0]
        pos_tue = positions[1][0]
        pos_wed = positions[2][0]
        pos_thu = positions[3][0]
        pos_fri = positions[4][0]

        lines_weekdays = {"mon": "", "tue": "", "wed": "", "thu": "", "fri": ""}
        # it must be lines[3:] instead of lines[2:] or else the menus would start with "Preis ab 0,90€" (from the
        # soups) instead of the first menu, if there is a day where the bistro is closed.
        for line in lines[soup_line_index + 3:]:
            lines_weekdays["mon"] += " " + line[pos_mon:pos_tue].replace("\n", " ")
            lines_weekdays["tue"] += " " + line[pos_tue:pos_wed].replace("\n", " ")
            lines_weekdays["wed"] += " " + line[pos_wed:pos_thu].replace("\n", " ")
            lines_weekdays["thu"] += " " + line[pos_thu:pos_fri].replace("\n", " ")
            lines_weekdays["fri"] += " " + line[pos_fri:].replace("\n", " ")

        for key in lines_weekdays:
            # get rid of two-character umlauts (e.g. SMALL_LETTER_A+COMBINING_DIACRITICAL_MARK_UMLAUT)
            lines_weekdays[key] = unicodedata.normalize("NFKC", lines_weekdays[key])
            # remove multi-whitespaces
            lines_weekdays[key] = ' '.join(lines_weekdays[key].split())
            # get all dish including name and price
            dish_names = re.findall(self.dish_regex, lines_weekdays[key] + " ")
            # get dish prices
            prices = re.findall(self.price_regex, ' '.join(dish_names))
            # convert prices to float
            prices = [float(price.replace("€", "").replace(",", ".").strip()) for price in prices]
            # remove price and commas from dish names
            dish_names = [re.sub(self.price_regex, "", dish).strip() for dish in dish_names]
            # create list of Dish objects
            dishes = [Dish(dish_name, price) for (dish_name, price) in list(zip(dish_names, prices), Ingredients("ipp-bistro"))]
            date = self.get_date(year, week_number, self.weekday_positions[key])
            # create new Menu object and add it to dict
            menu = Menu(date, dishes)
            # remove duplicates
            menu.remove_duplicates()
            menus[date] = menu

        return menus


class MedizinerMensaMenuParser(MenuParser):
    url = "https://www.med.fs.tum.de"

    def parse(self, location):
        page = requests.get(self.url)
        # get html tree
        tree = html.fromstring(page.content)
        # get url of current pdf menu
        xpath_query = tree.xpath("//a[contains(@href, 'KW_')]/@href")

        if len(xpath_query) != 1:
            return None
        pdf_url = self.url + xpath_query[0]

        # Example PDF-name: KW_44_Herbst_4_Mensa_2018.pdf
        pdf_name = pdf_url.split("/")[-1]
        wn_year_match = re.search("KW_([1-9]+\d*)_.*_(\d+).*", pdf_name, re.IGNORECASE)
        week_number = int(wn_year_match.group(1)) if wn_year_match else None
        year = int(wn_year_match.group(2)) if wn_year_match else None
        # convert 2-digit year into 4-digit year
        year = 2000 + year if year is not None and len(str(year)) == 2 else year

        with tempfile.NamedTemporaryFile() as temp_pdf:
            # download pdf
            response = requests.get(pdf_url)
            temp_pdf.write(response.content)
            with tempfile.NamedTemporaryFile() as temp_txt:
                # convert pdf to text by calling pdftotext; only convert first page to txt (-l 1)
                call(["pdftotext", "-l", "1", "-layout", temp_pdf.name, temp_txt.name])
                with open(temp_txt.name, 'r') as myfile:
                    # read generated text file
                    data = myfile.read()
                    menus = self.get_menus(data, year, week_number)
                    return menus

    def get_menus(self, text, year, week_number):
        menus = {}
        count = 0
        lines = text.replace("Extraessen", "").splitlines()
        for line in lines:
            if "Montag" in line:
                break

            count += 1

        lines = lines[count:]

        # get rid of Zusatzstoffe and Allergene: everything below the last ***-delimiter is irrelevant
        last_relevant_line = len(lines)
        for index, line in enumerate(lines):
            if "***" in line:
                last_relevant_line = index
        lines = lines[:last_relevant_line]

        days_list = [d for d in
                re.split(r"(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),\s\d{1,2}.\d{1,2}.\d{4}",
                         "\n".join(lines).replace("*", "").strip())
                if d not in ["", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]]
        if len(days_list) != 7:
            # as the Mediziner Mensa is part of hospital, it should serve food on each day
            return None
        days = {"mon": days_list[0], "tue": days_list[1], "wed": days_list[2], "thu": days_list[3], "fri": days_list[4],
                "sat": days_list[5], "sun": days_list[6]}


        for key in days:
            day_lines = unicodedata.normalize("NFKC", days[key]).splitlines(True)
            soup_str = ""
            mains_str = ""
            for day_line in day_lines:
                soup_str += day_line[:36].strip() + "\n"
                mains_str += day_line[40:100].strip() + "\n"

            soup = soup_str.replace("-\n", "").strip().replace("\n", " ")
            mains = [soup] + [m.strip().replace("\n", " ")
                              # https://regex101.com/r/MDFu1Z/1
                              for m in re.split(r"(\n{2,}|(?<!mit)\n(?=[A-Z]))", mains_str) if m is not ""]
            mains = [re.sub(r"\s(([A-Z]|\d),?)+\s?(?!(\w|\d))", "", m.replace("€", "")).strip()
                     for m in mains if m not in ["", "Feiertag"]]
            # TODO prices
            dishes = [Dish(dish_name, "N/A", Ingredients("mediziner-mensa")) for dish_name in mains]
            date = self.get_date(year, week_number, self.weekday_positions[key])
            menu = Menu(date, dishes)
            # remove duplicates
            menu.remove_duplicates()
            menus[date] = menu

        return menus
