# -*- coding: utf-8 -*-

import json


class Dish:
    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients

    def __repr__(self):
        if type(self.price) is not str:
            return "%s %s: %.2f€" % (self.name, str(list(self.ingredients)), self.price)
        else:
            return "%s %s: %s" % (self.name, str(list(self.ingredients)), self.price)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.name == other.name
                    and self.price == other.price
                    and self.ingredients == other.ingredients)
        return False

    def to_json_obj(self):
        return {"name": self.name, "price": self.price,
             "ingredients": list(self.ingredients)}

    def __hash__(self):
        # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
        return (hash(self.name) << 1) ^ hash(self.price) ^ hash(frozenset(self.ingredients))


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

    def remove_duplicates(self):
        unique = []
        seen = set()

        for d in self.dishes:
            if d not in seen:
                unique.append(d)
                seen.add(d)

        self.dishes = unique


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

    def to_json_obj(self):
        return {"number": self.calendar_week, "year": self.year,
             "days": [{"date": str(menu.menu_date), "dishes": [dish.to_json_obj() for dish in menu.dishes]} for menu in
                      self.days]}

    def to_json(self):
        week_json = json.dumps(
            self.to_json_obj(),
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


class Ingredients:

    ingredient_lookup = {
        "GQB" : "Certified Quality - Bavaria",
        "MSC" : "Marine Stewardship Council",

        "1" : "with dyestuff",
        "2" : "with preservative",
        "3" : "with antioxidant",
        "4" : "with flavor enhancers",
        "5" : "sulphured",
        "6" : "blackened (olive)",
        "7" : "waxed",
        "8" : "with phosphate",
        "9" : "with sweeteners",
        "10" : "contains a source of phenylalanine",
        "11" : "with sugar and sweeteners",
        "13" : "with cocoa-containing grease",
        "14" : "with gelatin",
        "99" : "with alcohol",

        "f" : "meatless dish",
        "v" : "vegan dish",
        "S" : "with pork",
        "R" : "with beef",
        "K" : "with veal",
        "G" : "with poultry",  # mediziner mensa
        "W" : "with wild meat",  # mediziner mensa
        "L" : "with lamb",  # mediziner mensa
        "Kn" : "with garlic",
        "Ei" : "with chicken egg",
        "En" : "with peanut",
        "Fi" : "with fish",
        "Gl" : "with gluten-containing cereals",
        "GlW" : "with wheat",
        "GlR" : "with rye",
        "GlG" : "with barley",
        "GlH" : "with oats",
        "GlD" : "with spelt",
        "Kr" : "with crustaceans",
        "Lu" : "with lupines",
        "Mi" : "with milk and lactose",
        "Sc" : "with shell fruits",
        "ScM" : "with almonds",
        "ScH" : "with hazelnuts",
        "ScW" : "with Walnuts",
        "ScC" : "with cashew nuts",
        "ScP" : "with pistachios",
        "Se" : "with sesame seeds",
        "Sf" : "with mustard",
        "Sl" : "with celery",
        "So" : "with soy",
        "Sw" : "with sulfur dioxide and sulfites",
        "Wt" : "with mollusks",
    }
    """A dictionary of all ingredients (from the Studentenwerk) with their description."""

    fmi_ingredient_lookup = {
        "Gluten" : "Gl",
        "Laktose" : "Mi",
        "Milcheiweiß" : "Mi",
        "Milch" : "Mi",
        "Ei" : "Ei",
        "Hühnerei" : "Ei",
        "Soja" : "So",
        "Nüsse" : "Sc",
        "Erdnuss" : "En",
        "Sellerie" : "Sl",
        "Fisch" : "Si",
        "Krebstiere" : "Kr",
        "Weichtiere" : "Wt",
        "Sesam" : "Se",
        "Senf" : "Sf",
    }

    mediziner_ingredient_lookup = {
        "1" : "1",
        "2" : "2",
        "3" : "3",
        "4" : "4",
        "5" : "5",
        "6" : "6",
        "7" : "7",
        "8" : "8",
        "9" : "9",

        "A" : "99",
        "B" : "Gl",
        "C" : "Kr",
        "E" : "Fi",
        "F" : "Fi",
        "G" : "G",
        "H" : "En",
        "K" : "K",
        "L" : "L",
        "M" : "So",
        "N" : "Mi",
        "O" : "Sc",
        "P" : "Sl",
        "R" : "R",
        "S" : "S",
        "T" : "Sf",
        "U" : "Se",
        "V" : "Sw",
        "W" : "W",
        "X" : "Lu",
        "Y" : "Ei",
        "Z" : "Wt",
    }

    def __init__(self, location):
        self.location = location
        self.ingredient_set = set()

    def parse_ingredients(self, values):
        values = values.strip()
        # check for special parser/ingredient translation required
        if self.location == "fmi-bistro":
            self.parse_lookup_ingredients(values, self.fmi_ingredient_lookup)
        elif self.location == "mediziner-mensa":
            self.parse_lookup_ingredients(values, self.mediziner_ingredient_lookup)
        # default to the "Studentenwerk" ingredients
        # "ipp-bistro" also uses the "Studentenwerk" ingredients since all
        # dishes contain the same ingredients
        else:
            split_values = values.split(",")
            for value in split_values:
                # ignore empty values
                if not value or value.isspace():
                    continue
                if not value in self.ingredient_lookup:
                    print("Unknown ingredient for " + self.location + " found: " + str(value))
                    continue
                self.ingredient_set.add(value)
    
    def parse_lookup_ingredients(self, values, lookup):
        split_values = values.split(",")
        for value in split_values:
            # ignore empty values
            if not value or value.isspace():
                continue
            if not value in lookup:
                print("Unknown ingredient for " + self.location + " found: " + str(value))
                continue
            self.ingredient_set.add(lookup[value])

    def __hash__(self):
        return hash(frozenset(self.ingredient_set))