"""
Some time format convert functions
"""

import time
import sys

import datetime
from datetime import timedelta
from datetime import datetime as dt

from log_control import log_main

import _config
import config


sys.path.append(_config.SEN_CONFIG.data_location)

TIMT_FORMAT = "%Y-%m-%d"
LOGGER = log_main('log_helper')

def time_convert(time_string):
    """
    A utility function, convert string to datetime
    Input: time_string(string)
    Return: time_mark(datetime)
    """
    # LOGGER.debug('ENTRY: time_convert() time_string: '+ time_string)
    tmp = time_string.replace('u', '')
    tmp = time_string.replace(',', '')
    tmp = tmp.replace('th', '')
    try:
        time_mark = time.strptime(tmp, "%b %d %Y")
        return time_mark
    except Exception as err:
        time_mark = time.strptime(tmp, "%B %d %Y")
        return time_mark

def get_time_marker(past_days=-5):
    """
    Get datetime type return of last 5 days
    Input: past_days(int)
    Return: (datetime)
    """
    date = dt.today().date()
    # this variable determine how many day do we check backward for the updates
    date += timedelta(past_days)
    LOGGER.debug('get_time_marker() %s', str(time.strptime(str(date), TIMT_FORMAT)))
    return time.strptime(str(date), TIMT_FORMAT)

def create_time_check_string():
    """
    Get EST time and a time string without format
    Input:
    Return: time_check(datetime), str(string)
    """
    #utc to ESTs
    time_check = datetime.datetime.utcnow() - datetime.timedelta(0, 4*3600) #utc to ESTs
    return time_check, str(time_check.year)+str(time_check.month)+str(time_check.day)+str(time_check.hour)
