# -*- coding: utf-8 -*-

import requests
import re
import unicodedata
import tempfile
from datetime import datetime
from lxml import html
from subprocess import call

import util
from entities import Dish, Menu


class MenuParser:
    def parse(self, location):
        pass


class StudentenwerkMenuParser(MenuParser):
    prices = {
        "Tagesgericht 1": 1, "Tagesgericht 2": 1.55, "Tagesgericht 3": 1.9, "Tagesgericht 4": 2.4,
        "Aktionsessen 1": 1.55, "Aktionsessen 2": 1.9, "Aktionsessen 3": 2.4, "Aktionsessen 4": 2.6,
        "Aktionsessen 5": 2.8, "Aktionsessen 6": 3.0, "Aktionsessen 7": 3.2, "Aktionsessen 8": 3.5, "Aktionsessen 9": 4,
        "Aktionsessen 10": 4.5, "Biogericht 1": 1.55, "Biogericht 2": 1.9, "Biogericht 3": 2.4, "Biogericht 4": 2.6,
        "Biogericht 5": 2.8, "Biogericht 6": 3.0, "Biogericht 7": 3.2, "Biogericht 8": 3.5, "Biogericht 9": 4,
        "Biogericht 10": 4.5, "Self-Service": "Self-Service", "Self-Service Grüne Mensa": "Self-Service Grüne Mensa",
        "Baustellenteller": "Baustellenteller (2.40€ - 3.45€)", "Fast Lane": "Fast Lane (3.50€ - 5.20€)"
    }
    links = {
        "mensa-garching": 'http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_422_-de.html',
        "mensa-arcisstrasse": "http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_421_-de.html",
        "stubistro-grosshadern": "http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_414_-de.html"
    }

    def parse(self, location):
        page_link = self.links.get(location, "")
        if page_link != "":
            page = requests.get(page_link)
            tree = html.fromstring(page.content)
            return self.get_menus(tree)
        else:
            return None

    def get_menus(self, page):
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
            dishes = self.__parse_dishes(menu_html)
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
    def __parse_dishes(menu_html):
        # obtain the names of all dishes in a passed menu
        dish_names = [dish.rstrip() for dish in menu_html.xpath("//p[@class='js-schedule-dish-description']/text()")]
        # make duplicates unique by adding (2), (3) etc. to the names
        dish_names = util.make_duplicates_unique(dish_names)
        # obtain the types of the dishes (e.g. 'Tagesgericht 1')
        dish_types = [type.text if type.text else '' for type in menu_html.xpath("//span[@class='stwm-artname']")]
        # create dictionary out of dish name and dish type
        dishes_dict = {dish_name: dish_type for dish_name, dish_type in zip(dish_names, dish_types)}
        # create Dish objects with correct prices; if price is not available, -1 is used instead
        dishes = [Dish(name, StudentenwerkMenuParser.prices.get(dishes_dict[name], "N/A")) for name in dishes_dict]
        return dishes

class FMIBistroMenuParser(MenuParser):
    url = "http://www.wilhelm-gastronomie.de/tum-garching"
    allergens = ["Gluten", "Laktose", "Milcheiweiß", "Hühnerei", "Soja", "Nüsse", "Erdnuss", "Sellerie", "Fisch",
                 "Krebstiere", "Weichtiere", "Sesam", "Senf", "Milch", "Ei"]
    weekday_positions = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5}
    price_regex = r"\€\s\d+,\d+"
    dish_regex = r".+?\€\s\d+,\d+"

    def parse(self, location):
        menus = None
        # get web page of bistro
        page = requests.get(self.url)
        # get html tree
        tree = html.fromstring(page.content)
        # get url of current pdf menu
        xpath_query = tree.xpath("//a[contains(text(), 'Garching-Speiseplan')]/@href")
        pdf_url = xpath_query[0] if len(xpath_query) == 1 else None

        if pdf_url is None:
            return None

        # Example PDF-name: Garching-Speiseplan_KW46_2017.pdf
        pdf_name = pdf_url.split("/")[-1]
        year = int(pdf_name.split("_")[-1].split(".")[0])
        week_number = int(pdf_name.split("_")[1].replace("KW","").lstrip("0"))

        with tempfile.NamedTemporaryFile() as temp_pdf:
            # download pdf
            response = requests.get(pdf_url)
            temp_pdf.write(response.content)
            with tempfile.NamedTemporaryFile() as temp_txt:
                # convert pdf to text by callinf pdftotext
                call(["pdftotext", "-layout", temp_pdf.name, temp_txt.name])
                with open(temp_txt.name, 'r') as myfile:
                    # read generated text file
                    data = myfile.read()
                    menus = self.get_menus(data, year, week_number)

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
            dish_names = [re.sub(self.price_regex, "", dish).replace("," ,"").strip() for dish in dish_names]
            # create list of Dish objects; only take first 3 as the following dishes are corrupt and not necessary
            dishes = [Dish(dish_name, price) for (dish_name, price) in list(zip(dish_names, prices))][:3]
            # get date from year, week number and current weekday
            # https://stackoverflow.com/questions/17087314/get-date-from-week-number
            date_str = "%d-W%d-%d" % (year, week_number, self.weekday_positions[key])
            date = datetime.strptime(date_str, "%Y-W%W-%w").date()
            # create new Menu object and add it to dict
            menu = Menu(date, dishes)
            # remove duplicates
            menu.remove_duplicates()
            menus[date] = menu

        return menus


class IPPBistroMenuParser(MenuParser):
    url = "http://konradhof-catering.de/ipp/"
    weekday_positions = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5}
    price_regex = r"\d+,\d+\s\€[^\)]"
    dish_regex = r".+?\d+,\d+\s\€[^\)]"

    def parse(self, location):
        page = requests.get(self.url)
        # get html tree
        tree = html.fromstring(page.content)
        # get url of current pdf menu
        xpath_query = tree.xpath("//a[contains(text(), 'KW-')]/@href")
        pdf_url = xpath_query[0] if len(xpath_query) >= 1 else None

        if pdf_url is None:
            return None

        # Example PDF-name: KW-48_27.11-01.12.10.2017-3.pdf
        pdf_name = pdf_url.split("/")[-1]
        year = int(pdf_name.replace(".pdf","").split(".")[-1].split("-")[0])
        week_number = int(pdf_name.split("_")[0].replace("KW-","").lstrip("0"))

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
        lines = text.splitlines()
        count = 0
        # remove headline etc.
        for line in lines:
            if line.replace(" ", "").replace("\n", "").lower() == "montagdienstagmittwochdonnerstagfreitag":
                break

            count += 1

        lines = lines[count:]
        weekdays = lines[0]
        lines = lines[3:]

        positions = [(a.start(), a.end()) for a in list(re.finditer('Tagessuppe siehe Aushang', lines[0]))]
        if len(positions) != 5:
            # TODO handle special cases (e.g. that bistro is closed)
            return None

        pos_mon = positions[0][0]
        pos_tue = positions[1][0]
        pos_wed = positions[2][0]
        pos_thu = positions[3][0]
        pos_fri = positions[4][0]

        lines_weekdays = {"mon": "", "tue": "", "wed": "", "thu": "", "fri": ""}
        for line in lines[2:]:
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
            dishes = [Dish(dish_name, price) for (dish_name, price) in list(zip(dish_names, prices))]
            # get date from year, week number and current weekday
            # https://stackoverflow.com/questions/17087314/get-date-from-week-number
            date_str = "%d-W%d-%d" % (year, week_number, self.weekday_positions[key])
            date = datetime.strptime(date_str, "%Y-W%W-%w").date()
            # create new Menu object and add it to dict
            menu = Menu(date, dishes)
            # remove duplicates
            menu.remove_duplicates()
            menus[date] = menu

        return menus
