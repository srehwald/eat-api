# -*- coding: utf-8 -*-

from datetime import datetime

date_pattern = "%d.%m.%Y"
format = "dd.mm.yyyy"


def parse_date(date_str):
    return datetime.strptime(date_str, date_pattern).date()
