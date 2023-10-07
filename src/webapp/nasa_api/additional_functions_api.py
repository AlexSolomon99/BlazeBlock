from datetime import datetime, timedelta

def convert_datetime_to_day_string(dateime_date: datetime):

    time_format = r"%Y-%m-%d"

    year_month_day = dateime_date.strftime(time_format)
    return year_month_day

def convert_ymd_string_to_datetime(ymd_string: str):
    time_format = r"%Y-%m-%d"
    ymd_datetime = datetime.strptime(ymd_string, time_format)

    return ymd_datetime

