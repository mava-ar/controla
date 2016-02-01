import calendar
from datetime import datetime, timedelta

from django.utils import timezone


def get_30_days():
    # Get the current date (00:00:00:00 in time)
    current_tz = timezone.get_current_timezone()
    current_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=current_tz)
    return current_date - timedelta(days=30), current_date


def get_current_month():
    """
    Return tz aware datetimes for the first and last day of the current month.
    """
    # Get the current date (00:00:00:00 in time)
    current_tz = timezone.get_current_timezone()
    current_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=current_tz)

    # Calculate the first day of the month
    first_day = current_date - timedelta(days=current_date.day - 1)

    # Now calculate the last day of the month
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    last_day = first_day + timedelta(days=days_in_month - 1)

    return first_day, last_day


def datetime_to_date(date):
    try:
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    except TypeError:
        # to_date is a datetime.date
        pass
    return date


def format_date(date, dt_format="%d/%m/%Y"):
    """Return a string formatted for the given date."""
    try:
        return datetime.strftime(date, dt_format)
    except ValueError:
        try:
            return datetime.strftime(date, "%d/%m/%y")
        except ValueError:
            return None


def now_timestamp():
    return calendar.timegm(datetime.now().timetuple())