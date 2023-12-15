from datetime import datetime
import pytz

def determiner():
    workday_morning = datetime.strptime('09:00:00.000000', '%H:%M:%S.%f').time()
    workday_evening = datetime.strptime('18:00:00.000000', '%H:%M:%S.%f').time()
    weekend_morning = datetime.strptime('10:00:00.000000', '%H:%M:%S.%f').time()
    weekend_evening = datetime.strptime('22:00:00.000000', '%H:%M:%S.%f').time()
    date = datetime.date(datetime.now(pytz.timezone('Europe/Moscow')))
    week_day = date.weekday()
    now = datetime.now(pytz.timezone('Europe/Moscow')).time()

    if week_day>4 and week_day<7:
        if now < workday_morning or now > workday_evening:
            return True
        else:
            return False
    else:
        if now < workday_morning or now > workday_evening:
            return True
        else:
            return False
