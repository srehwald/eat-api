from pyopenmensa.feed import LazyBuilder
from datetime import date

def openmensa(weeks, directory):
    canteen = weeksToCanteenFeed(weeks)

    writeFeedToFile(canteen, directory)

def weeksToCanteenFeed(weeks):
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
                addDishToCanteen(dish, menu.menu_date, canteen)

    return canteen

def addDishToCanteen(dish, date, canteen):
    if type(dish.price) is float:
        prices = {'other': dish.price}
    else:
        prices = {}
    canteen.addMeal(date, 'Speiseplan', dish.name, prices=prices)

def writeFeedToFile(canteen, directory):
    with open("%s/feed.xml" % (str(directory)), 'w') as outfile:
        outfile.write(canteen.toXMLFeed())
