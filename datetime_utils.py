"""
Author: Adam Knowles
Version: 0.1
Name: datetime_utils.py
Description: Utils that operate on datetime

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import utime # type: ignore
import ntptime # type: ignore
import uasyncio
import urandom  # type: ignore
import config
import utils
import machine # type: ignore

def format_date(dt):
    # Format the date as 'DD MMM YYYY'.
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day = "{:02d}".format(dt[2])
    month = months[dt[1] - 1]
    year = "{:04d}".format(dt[0])
    return f"{day} {month} {year}"

def last_sunday(year, month):
    # Calculate the date of the last Sunday of the specified month and year.
    # Find the date of the last Sunday in a given month
    last_day = utime.mktime((year, month + 1, 1, 0, 0, 0, 0, 0)) - 86400  # Set to the last day of the previous month
    weekday = utime.localtime(last_day)[6]  # Get the weekday for the last day

    while weekday != 6:  # Sunday has index 6
        last_day -= 86400  # Subtract a day in seconds
        weekday = (weekday - 1) % 7
    return int(last_day)

def is_DST(timestamp):
    # Check if the current time is within BST (British Summer Time).
    # Check if the given timestamp is in DST (BST) considering the 1 am transition
    time_tuple = utime.localtime(timestamp)
    dst_start = last_sunday(time_tuple[0], 3)  # Last Sunday of March
    dst_end = last_sunday(time_tuple[0], 10)   # Last Sunday of October

    # Check if the current time is within DST dates
    if dst_start <= timestamp < dst_end:
        # Check if it's after 1 am on the last Sunday of March and before 2 am on the last Sunday of October
        if (time_tuple[1] == 3 and time_tuple[2] == (dst_start // 86400) + 1 and time_tuple[3] < 1) or (time_tuple[1] == 10 and time_tuple[2] == (dst_end // 86400) and time_tuple[3] < 2):
            return False  # Not in DST during the 1 am transition
        else:
            return True   # In DST during other times
    else:
        return False
    
def get_time_values(current_time_tuple=None):
    # Split a time into individual digits, defaulting to current, real time.
    if current_time_tuple is None:
        current_time_tuple = utime.localtime()

    # Extract digits
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day_of_month = current_time_tuple[2]
    month_name = month_names[current_time_tuple[1] - 1]
    year = current_time_tuple[0]
    hours_tens, hours_ones = divmod(current_time_tuple[3], 10)
    minutes_tens, minutes_ones = divmod(current_time_tuple[4], 10)
    seconds_tens, seconds_ones = divmod(current_time_tuple[5], 10)

    # Return the extracted digits
    return (
        hours_tens, hours_ones,
        minutes_tens, minutes_ones,
        seconds_tens, seconds_ones,
        day_of_month, month_name, year,
    )

def sync_rtc():
    # Assuming Wifi is already connected, sync RTC to NTP, then add an hour if it's DST and update the RTC
    # try:
        if not utils.is_wifi_connected():
            raise Exception("Wi-Fi is not connected")

        ntptime.settime()

        # Work out if we're in DST and if so, add an hour to the RTC
        current_timestamp = utime.time()

        is_DST_flag = is_DST(current_timestamp)

        if is_DST_flag:
            current_timestamp += 3600

        # print(f"current_timestamp: {current_timestamp} and as tuple: {utime.localtime(current_timestamp)}")
        rtc = machine.RTC()
        # rtc.datetime() param is a different format of tuple to utime.localtime() so below converts it
        rtc.datetime((utime.localtime(current_timestamp)[0], utime.localtime(current_timestamp)[1], utime.localtime(current_timestamp)[2], utime.localtime(current_timestamp)[6], utime.localtime(current_timestamp)[3], utime.localtime(current_timestamp)[4], utime.localtime(current_timestamp)[5], 0))
        print(f"RTC time set from NTP with DST: {is_DST_flag} ")
    # except Exception as e:
    #     print(f"Failed to set time: {e}")
    #     pass
    
async def sync_rtc_periodically():
    while True:
        # print("sync_ntp_periodically() called")
        sync_rtc()
        current_time = utime.localtime()
         
        # Calculate seconds until the top of the next hour, then add a random offset
        next_sync_secs = 3600 - current_time[5] - (60 * current_time[4]) + urandom.randint(0, 59)
        
        print(f"sync_ntp_periodically() complete. Next sync in (secs): {next_sync_secs} secs")
        await uasyncio.sleep(next_sync_secs)  # Sleep for the calculated duration