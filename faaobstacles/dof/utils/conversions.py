from datetime import datetime, timedelta

ACCURACY_CODE_TO_FEET = {
    '1': 20.0,
    '2': 50.0,
    '3': 100.0,
    '4': 250.0,
    '5': 500.0,
    '6': 1000.0,
    '7': 3038.6,
    '8': 6076.12,
    '9': None,
    'A': 3.0,
    'B': 10.0,
    'C': 20.0,
    'D': 50.0,
    'E': 125.0,
    'F': 250.0,
    'G': 500.0,
    'H': 1000.0,
    'I': None,
    ' ': None,
}

def julian_to_date(date_str):
    year = date_str[:4]
    num_days = int(date_str[4:]) - 1
    day_frmt = '%m/%d/%Y'

    init_day = datetime.strptime(
        '01/01/{0}'.format(year),
        day_frmt
    ).date()

    offset_day = init_day + timedelta(days=num_days)

    return offset_day
