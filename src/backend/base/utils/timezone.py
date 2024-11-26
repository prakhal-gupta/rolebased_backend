from datetime import timedelta, date
import calendar
import numpy as np
import pandas as pd
import pytz

from dateutil.parser import parse
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def now_local(only_date=False):
    tz = 'Asia/Kolkata'
    timezone.activate(pytz.timezone(tz))
    if only_date:
        result = (timezone.localtime(timezone.now())).date()
    else:
        result = (timezone.localtime(timezone.now()))
    timezone.activate(pytz.timezone('UTC'))
    return result


def get_boundaries_for_tomorrow_and_day_after_tomorrow():
    today = timezone.now_local(only_date=True)
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = tomorrow + timedelta(days=1)
    return tomorrow, day_after_tomorrow


def localtime(date_obj):
    return timezone.localtime(date_obj)


def to_localtime(date_obj):
    tz = 'Asia/Kolkata'
    timezone.activate(pytz.timezone(tz))
    result = (timezone.localtime(date_obj))
    timezone.activate(pytz.timezone('UTC'))
    return result


def get_today_start():
    return now_local().replace(hour=0, minute=0, second=0, microsecond=0)


def get_today_end():
    tomorrow = get_today_start() + timedelta(days=1)
    return tomorrow - timedelta(microseconds=1)


def get_day_start(date):
    from datetime import datetime
    date_time = datetime.combine(date, datetime.min.time())
    return date_time.replace(hour=0, minute=0, second=0, microsecond=0)


def get_day_end(date):
    from datetime import datetime
    date_time = datetime.combine(date, datetime.min.time())
    return date_time.replace(hour=23, minute=59, second=59, microsecond=0)


def get_yesterday_boundaries():
    yesterday_start = get_today_start() - timedelta(days=1)
    yesterday_end = get_today_start() - timedelta(microseconds=1)
    return yesterday_start, yesterday_end


def get_current_month_start():
    return get_today_start().replace(day=1)


def get_prev_month_boundaries():
    prev_month_end_date = get_current_month_start() - timedelta(microseconds=1)
    if prev_month_end_date:
        prev_month_start_date = prev_month_end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return prev_month_start_date, prev_month_end_date


def get_prev_month_till_today():
    prev_month_start_date, prev_month_end_date = get_prev_month_boundaries()
    try:
        prev_month_end_till_date = prev_month_end_date.replace(
            day=get_today_start().day)
    except ValueError:
        prev_month_end_till_date = prev_month_end_date
    return prev_month_start_date, prev_month_end_till_date


def get_next_60_days_date():
    return now_local(only_date=True) + timedelta(days=59)


def get_dates(start_date, end_date=None):
    try:
        startdate = start_date.date()
        enddate = end_date.date() if end_date else end_date
        date_dict = {
            # Date display
            "start_date": startdate,
            "end_date": enddate,
        }
    except AttributeError:
        date_dict = {
            "start_date": start_date,
            "end_date": end_date
        }
    return date_dict


def get_contest_date(start_date=None, end_date=None):
    from datetime import datetime
    from pytz import timezone
    date_str = "2017-10-01 00:00:01"
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('Asia/Kolkata'))
    return datetime_obj_utc


def get_date_format_for_reports_string(date_str):
    from datetime import datetime
    from pytz import timezone
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    datetime_obj_utc = datetime_obj.replace(tzinfo=timezone('Asia/Kolkata'))
    return datetime_obj_utc


def get_next_prev_year_month_start_end_date():
    from calendar import monthrange
    from dateutil.relativedelta import relativedelta
    prev_year_month_start_date = get_current_month_start() - timedelta(microseconds=-1)
    pre_policy_start_date = prev_year_month_start_date - relativedelta(years=1)
    first_day = pre_policy_start_date.replace(hour=0, minute=0, second=0, microsecond=1)
    get_month_days = monthrange(prev_year_month_start_date.year, prev_year_month_start_date.month)
    days_in_month = get_month_days[1]
    last_day = pre_policy_start_date.replace(day=days_in_month, hour=23, minute=59, second=59, microsecond=1)
    return first_day, last_day


def to_str(dt):
    if not dt:
        return dt
    return dt.isoformat()


def from_str(dt_str):
    if not dt_str:
        return dt_str
    return parse(dt_str)


def get_the_last_date_of_month(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return date.replace(day=last_day)


def subtract_years(date=None, years=1):
    import datetime
    if isinstance(date, datetime.date):
        return date.replace(year=date.year - years)
    else:
        current_datetime = now_local()
        return current_datetime.replace(year=current_datetime.year - years)


def get_current_month_no_of_days():
    import datetime
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def get_date_difference(start_date, end_date=None):
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.combine(end_date, datetime.min.time())
    start_date = datetime.combine(start_date, datetime.min.time())
    difference = relativedelta(end_date, start_date)
    return {'years': difference.years, 'months': difference.months, 'days': difference.days}


def get_month_end_date_and_start_date(month, year=now_local().year):
    start_date = now_local().replace(day=1, year=year, month=month, hour=0, minute=0, second=0, microsecond=0)
    if month == 12:
        end_date = start_date.replace(month=1, year=year + 1) - timedelta(microseconds=1)
    elif month == 1:
        end_date = start_date.replace(day=31, month=month, year=year)
    else:
        end_date = start_date.replace(month=month + 1) - timedelta(microseconds=1)
    return start_date, end_date


def get_back_months_ago(no_of_month):
    return date.today() + relativedelta(months=-no_of_month)


def get_n_times_back_to_months(date, no_of_month):
    return date + relativedelta(months=-no_of_month)


def time_elapsed(end_time, start_time):
    from datetime import datetime
    end_date = datetime.combine(now_local(), end_time)
    start_date = datetime.combine(now_local(), start_time)
    difference = end_date - start_date
    return difference


def all_date_in_daterange(date1, date2):
    x = []
    for n in range(0, int((date2 - date1).days) + 1):
        x.append(date1 + timedelta(n))
    return x


def filter_date_by_date_range(date_list, date1, date2):
    date = []
    for one in date_list:
        if date1 <= one <= date2 and one not in date:
            date.append(one)
    return date


def days_in_date_range(date1, date2, weekdays):
    all_date = all_date_in_daterange(date1, date2)
    req_date = []
    for dt in all_date:
        if dt.isoweekday() in weekdays:
            req_date.append(dt.strftime("%Y-%m-%d"))
    return req_date


def get_weekday_number_of_a_date_in_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    weekday_no = np.where(x == day)[0][0] + 1
    return (weekday_no)


def odd_days_in_date_range(date1, date2, weekdays, even=False):
    req_date = []
    all_date = days_in_date_range(date1, date2, weekdays)
    calendar.setfirstweekday(6)
    if even:
        for one in all_date:
            one_date = pd.to_datetime(one)
            week_no = get_weekday_number_of_a_date_in_month(one_date.year, one_date.month, one_date.day)
            if week_no % 2 == 0:
                req_date.append(one_date.strftime("%Y-%m-%d"))
    else:
        for one in all_date:
            one_date = pd.to_datetime(one)
            week_no = get_weekday_number_of_a_date_in_month(one_date.year, one_date.month, one_date.day)
            if week_no % 2 == 1:
                req_date.append(one_date.strftime("%Y-%m-%d"))
    return req_date


def get_days_difference(start, end):
    start = pd.to_datetime(start).date()
    end = pd.to_datetime(end).date()
    total_days = (end - start).days + 1
    return total_days


def get_hours_minutes_from_timedelta(time):
    days = time.days if time and time.days else 0
    seconds = time.seconds if time and time.seconds else 0
    total_seconds = (days * 24 * 60 * 60) + seconds
    minutes = (total_seconds % 3600) // 60
    return {"hours": total_seconds // 3600, "minutes": minutes if minutes > 9 else "0" + str(minutes)}


def add_time(time1, time2):
    if time1 and time2:
        a = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
        b = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)
        return a + b
    elif time1:
        return timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
    elif time2:
        return timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)
    return None
