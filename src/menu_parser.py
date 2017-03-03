# -*- coding: utf-8 -*-

from lxml import html
import requests
from datetime import datetime


class Dish:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "%s: %d€" % (self.name, self.price)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.price == other.price
        return False

    def __hash__(self):
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return (hash(self.name) << 1) ^ hash(self.price)


class Menu:
    def __init__(self, menu_date, dishes):
        self.menu_date = menu_date
        self.dishes = dishes

    def __repr__(self):
        menu_str = str(self.menu_date) + ": " + str(self.dishes)
        return menu_str

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            dishes_equal = set(self.dishes) == set(other.dishes)
            date_equal = self.menu_date == other.menu_date
            return dishes_equal and date_equal
        return False


class MenuParser:
    def parse(self, location):
        pass


class StudentenwerkMenuParser(MenuParser):
    # format for date used in the Studentenwerk menu
    date_format = "%d.%m.%Y"
    prices = {
        "Tagesgericht 1": 1, "Tagesgericht 2": 1.55, "Tagesgericht 3": 1.9, "Tagesgericht 4": 2.4,
        "Aktionsessen 1": 1.55, "Aktionsessen 2": 1.9, "Aktionsessen 3": 2.4, "Aktionsessen 4": 2.6,
        "Aktionsessen 5": 2.8, "Aktionsessen 6": 3.0, "Aktionsessen 7": 3.2, "Aktionsessen 8": 3.5, "Aktionsessen 9": 4,
        "Aktionsessen 10": 4.5, "Biogericht 1": 1.55, "Biogericht 2": 1.9, "Biogericht 3": 2.4, "Biogericht 4": 2.6,
        "Biogericht 5": 2.8, "Biogericht 6": 3.0, "Biogericht 7": 3.2, "Biogericht 8": 3.5, "Biogericht 9": 4,
        "Biogericht 10": 4.5,
    }
    links = {
        "mensa-garching": 'http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_422_-de.html'
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
            current_menu_date_str = menu_html.xpath("//table/tr[1]/td[2]/span[1]/a[1]/strong/text()")[0].split()[1]

            #TODO handle parsing error
            current_menu_date = datetime.strptime(current_menu_date_str, '%d.%m.%Y').date()
            # parse dishes of current menu
            dishes = self.__parse_dishes(menu_html)
            # create menu object
            menu = Menu(datetime.strptime(current_menu_date_str, self.date_format).date(), dishes)
            # add menu object to dictionary using the date as key
            menus[current_menu_date] = menu

        # return the menu for the requested date; if no menu exists, None is returned
        return menus

    @staticmethod
    def __get_daily_menus_as_html(page):
        # obtain all daily menus found in the passed html page by xpath query
        daily_menus = page.xpath("//table[@class='menu']")
        return daily_menus

    @staticmethod
    def __parse_dishes(menu_html):
        # obtain the names of all dishes in a passed menu
        dish_names = menu_html.xpath("//table/tr/td[@class='beschreibung']/span[1]/text()")
        # obtain the types of the dishes (e.g. 'Tagesgericht 1')
        dish_types = menu_html.xpath("//table/tr/td[@class='gericht']/span[1]/text()")
        # create dictionary out of dish name and dish type
        dishes_dict = {dish_name: dish_type for dish_name, dish_type in zip(dish_names, dish_types)}
        # create Dish objects with correct prices; if price is not available, -1 is used instead
        dishes = [Dish(name, StudentenwerkMenuParser.prices.get(dishes_dict[name], -1)) for name in dishes_dict]
        return dishes