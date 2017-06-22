# from https://github.com/icholy/durationpy/blob/master/durationpy/duration.py

# Copyright 2017 Ilia Choly
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import math
import re
import datetime

_nanosecond_size  = 1
_microsecond_size = 1000 * _nanosecond_size
_millisecond_size = 1000 * _microsecond_size
_second_size      = 1000 * _millisecond_size
_minute_size      = 60   * _second_size
_hour_size        = 60   * _minute_size
_day_size         = 24   * _hour_size
_week_size        = 7    * _day_size
_month_size       = 30   * _day_size
_year_size        = 365  * _day_size

units = {
    "ns": _nanosecond_size,
    "us": _microsecond_size,
    "µs": _microsecond_size,
    "μs": _microsecond_size,
    "ms": _millisecond_size,
    "s":  _second_size,
    "m":  _minute_size,
    "h":  _hour_size,
    "d":  _day_size,
    "w":  _week_size,
    "mm": _month_size,
    "y":  _year_size,
}


def from_str(duration):
    """Parse a duration string to a datetime.timedelta"""

    if duration in ("0", "+0", "-0"):
        return datetime.timedelta()

    pattern = re.compile('([\d\.]+)([a-zµμ]+)')
    total = 0
    sign = -1 if duration[0] == '-' else 1
    matches = pattern.findall(duration)

    if not len(matches):
        raise Exception("Invalid duration {}".format(duration))

    for (value, unit) in matches:
        if unit not in units:
            raise Exception(
                "Unknown unit {} in duration {}".format(unit, duration))
        try:
            total += float(value) * units[unit]
        except:
            raise Exception(
                "Invalid value {} in duration {}".format(value, duration))

    microseconds = total / _microsecond_size
    return datetime.timedelta(microseconds=sign * microseconds)

def to_str(delta, extended=False):
    """Format a datetime.timedelta to a duration string"""

    total_seconds = delta.total_seconds()
    sign = "-" if total_seconds < 0 else ""
    nanoseconds = abs(total_seconds * _second_size)

    if total_seconds < 1:
        result_str = _to_str_small(nanoseconds, extended)
    else:
        result_str = _to_str_large(nanoseconds, extended)

    return "{}{}".format(sign, result_str)


def _to_str_small(nanoseconds, extended):

    result_str = ""

    if not nanoseconds:
        return "0"

    milliseconds = int(nanoseconds / _millisecond_size)
    if milliseconds:
        nanoseconds -= _millisecond_size * milliseconds
        result_str += "{:g}ms".format(milliseconds)

    microseconds = int(nanoseconds / _microsecond_size)
    if microseconds:
        nanoseconds -= _microsecond_size * microseconds
        result_str += "{:g}us".format(microseconds)

    if nanoseconds:
        result_str += "{:g}ns".format(nanoseconds)

    return result_str


def _to_str_large(nanoseconds, extended):

    result_str = ""

    if extended:

        years = int(nanoseconds / _year_size)
        if years:
            nanoseconds -= _year_size * years
            result_str += "{:g}y".format(years)

        months = int(nanoseconds / _month_size)
        if months:
            nanoseconds -= _month_size * months
            result_str += "{:g}mm"

        days = int(nanoseconds / _day_size)
        if days:
            nanoseconds -= _day_size * days
            result_str += "{:g}d"

    hours = int(nanoseconds / _hour_size)
    if hours:
        nanoseconds -= _hour_size * hours
        result_str += "{:g}h".format(hours)

    minutes = int(nanoseconds / _minute_size)
    if minutes:
        nanoseconds -= _minute_size * minutes
        result_str += "{:g}m".format(minutes)

    seconds = float(nanoseconds) / float(_second_size)
    if seconds:
        nanoseconds -= _second_size * seconds
        result_str += "{:g}s".format(seconds)

    return result_str


def get_time_till(sec,s):
    minutes = sec / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    months = weeks / 4
    years = months / 12
    minute = 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = week * 4
    year = month * 12
    if minutes < 1:
        return s

    time_amount = 0
    time_adjust = 0
    time_type = ""
    if years >= 1:
        time_amount = years
        time_adjust = year
        time_type = "year"
    elif months >= 1:
        time_amount = months
        time_adjust = month
        time_type = "month"
    elif weeks >= 1:
        time_amount = weeks
        time_adjust = week
        time_type = "week"
    elif days >= 1:
        time_amount = days
        time_adjust = day
        time_type = "day"
    elif hours >= 1:
        time_amount = hours
        time_adjust = hour

        time_type = "hour"
    else:
        time_amount = minutes
        time_adjust = minute
        time_type = "minute"
    if math.floor(time_amount) > 1:
        return ["%d %ss" % (time_amount,time_type)] + get_time_till(sec-math.floor(time_amount)*time_adjust,s)
    else:
        return ["%d %s" % (time_amount,time_type)] + get_time_till(sec-math.floor(time_amount)*time_adjust,s)


def get_total_time_string(total_time):
    the_times = get_time_till(total_time,[])
    if len(the_times) == 0:
        return 'no time'
    elif len(the_times) == 1:
        return ''.join(the_times)
    elif len(the_times) == 2:
        return ' and '.join(the_times)
    else:
        return ', '.join(the_times[:-1]) + ", and " +  the_times[-1]