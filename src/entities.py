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