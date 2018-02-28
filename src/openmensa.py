from pyopenmensa.feed import LazyBuilder
from datetime import date

def openmensa(weeks, directory):
    canteen = LazyBuilder() # canteen container
    # iterate through weeks
    for calendar_week in weeks:
        # get Week object
        week = weeks[calendar_week]
        # get year of calendar week
        days = week.days

        # iterate through days
        for menu in days:

            # iterate through dishes
            for dish in menu.dishes:
                if type(dish.price) is float:
                    prices = {'other': dish.price}
                else:
                    prices = {}
                canteen.addMeal(menu.menu_date, 'Speiseplan', dish.name, prices=prices)

    with open("%s/feed.xml" % (str(directory)), 'w') as outfile:
            outfile.write(canteen.toXMLFeed())
