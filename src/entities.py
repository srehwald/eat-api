# -*- coding: utf-8 -*-

import json


class Dish:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        if type(self.price) is not str:
            return "%s: %.2f€" % (self.name, self.price)
        else:
            return "%s: %s" % (self.name, self.price)

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


class Week:
    def __init__(self, calendar_week, year, days):
        self.calendar_week = calendar_week
        self.year = year
        self.days = days

    def __repr__(self):
        week_str = "Week %s-%s" % (self.year, self.calendar_week)
        for day in self.days:
            week_str += "\n %s" % day
        return week_str

    def to_json(self):
        week_json = json.dumps(
            {"number": self.calendar_week, "year": self.year,
             "days": [{"date": str(menu.menu_date), "dishes": [dish.__dict__ for dish in menu.dishes]} for menu in
                      self.days]},
            ensure_ascii=False, indent=4)
        return week_json

    @staticmethod
    def to_weeks(menus):
        weeks = {}
        for menu_key in menus:
            menu = menus[menu_key]
            menu_date = menu.menu_date
            # get calendar week
            calendar_week = menu_date.isocalendar()[1]
            # get year of the calendar week. watch out that for instance jan 01 can still be in week 52 of the
            # previous year
            year_of_calendar_week = menu_date.year - 1 \
                if calendar_week == 52 and menu_date.month == 1 else menu_date.year

            # append menus to respective week
            week = weeks.get(calendar_week, Week(calendar_week, year_of_calendar_week, []))
            week.days.append(menu)
            weeks[calendar_week] = week

        return weeks
