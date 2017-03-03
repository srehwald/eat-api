# -*- coding: utf-8 -*-

from datetime import datetime
import json

date_pattern = "%d.%m.%Y"
cli_date_format = "dd.mm.yyyy"


def parse_date(date_str):
    return datetime.strptime(date_str, date_pattern).date()


def to_json(menus):
    menu_jsons = json.dumps(
        [{"date": str(menu.menu_date), "dishes": [dish.__dict__ for dish in menu.dishes]} for menu in menus],
        ensure_ascii=False, indent=4)

    return menu_jsons
