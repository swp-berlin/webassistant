import re
import datetime as dt

import datefinder


def parse_date(date_str: str, default_date_str: str='1700-01-01') -> dt.date:
    date_str = ' '.join(date_str.split())
    default_date = dt.datetime.fromisoformat(default_date_str).date()
    if not date_str:
        return default_date
    try:
        return dt.datetime.fromisoformat(date_str).date()
    except ValueError:
        pass
    year = default_date.year
    years_found = re.findall(r'(19\d{2}|20\d{2})', date_str)
    if years_found:
        year = int(sorted(years_found)[0])
    if year != default_date.year:
        default_date = dt.date(year, 1, 1)
    dates_found = sorted([d.date() for d in datefinder.find_dates(date_str)])
    date = dates_found[0] if dates_found else None
    if date is None:
        return default_date
    if years_found and date.year != default_date.year:
        return default_date
    return date
