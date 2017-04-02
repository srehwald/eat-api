# -*- coding: utf-8 -*-

import requests
from lxml import html

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
        dish_names = menu_html.xpath("//p[@class='js-schedule-dish-description']/text()")
        # obtain the types of the dishes (e.g. 'Tagesgericht 1')
        dish_types = menu_html.xpath("//span[@class='stwm-artname']/text()")
        # create dictionary out of dish name and dish type
        dishes_dict = {dish_name: dish_type for dish_name, dish_type in zip(dish_names, dish_types)}
        # create Dish objects with correct prices; if price is not available, -1 is used instead
        dishes = [Dish(name.rstrip(), StudentenwerkMenuParser.prices.get(dishes_dict[name], -1)) for name in dishes_dict]
        return dishes
