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

def format_date(dt):
    """Format the date as 'DD MMM YYYY'."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day = "{:02d}".format(dt[2])
    month = months[dt[1] - 1]
    year = "{:04d}".format(dt[0])
    return f"{day} {month} {year}"

def last_sunday(year, month):
    """Calculate the date of the last Sunday of the specified month and year."""
    # Find the date of the last Sunday in a given month
    last_day = utime.mktime((year, month + 1, 1, 0, 0, 0, 0, 0)) - 86400  # Set to the last day of the previous month
    weekday = utime.localtime(last_day)[6]  # Get the weekday for the last day

    while weekday != 6:  # Sunday has index 6
        last_day -= 86400  # Subtract a day in seconds
        weekday = (weekday - 1) % 7
    return int(last_day)

def check_BST_active(dt):
    """Check if the current time is within BST (British Summer Time)."""
    # Check if the given datetime is in DST (BST) considering the 1 am transition
    dst_start = last_sunday(dt[0], 3)  # Last Sunday of March
    dst_end = last_sunday(dt[0], 10)   # Last Sunday of October

    # Check if the current time is within DST dates
    if dst_start <= utime.mktime(dt) < dst_end:
        # Check if it's after 1 am on the last Sunday of March and before 2 am on the last Sunday of October
        if (dt[1] == 3 and dt[2] == (dst_start // 86400) + 1 and dt[3] < 1) or (dt[1] == 10 and dt[2] == (dst_end // 86400) and dt[3] < 2):
            return False  # Not in DST during the 1 am transition
        else:
            return True   # In DST during other times
    else:
        return False
    
def get_time_values():
    """Get the current time and split it into individual digits."""
    current_time_tuple = utime.localtime()

    # If it's BST, add an hour to the current time
    if config.BST_active:
        current_time_seconds = utime.mktime(current_time_tuple)
        new_time_seconds = current_time_seconds + 3600
        current_time_tuple = utime.localtime(new_time_seconds)

    # Extract digits
    hours_tens, hours_ones = divmod(current_time_tuple[3], 10)
    minutes_tens, minutes_ones = divmod(current_time_tuple[4], 10)
    seconds_tens, seconds_ones = divmod(current_time_tuple[5], 10)

    # Return the extracted digits
    return (
        hours_tens, hours_ones,
        minutes_tens, minutes_ones,
        seconds_tens, seconds_ones
    )

def sync_ntp():
    """Turn on wifi, sync RTC to NTP, turn wifi off, return BST_active True or False."""
    # print('sync_ntp() called')
      
    try:
        if not utils.is_wifi_connected():
                    raise Exception("Wi-Fi is not connected")
        
        ntptime.settime() # No parameters available for DST offset
        # print("Time set from NTP")

        # Update the global BST status
        current_time_tuple = utime.localtime()
        config.BST_active = check_BST_active(current_time_tuple)
    except Exception as e:
        print(f"Failed to set time: {e}")
        pass

    # Disconnect from Wi-Fi
    #disconnect_wifi()
    
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.gu.update(config.picoboard)
    
async def sync_ntp_periodically():
    while True:
        # print("sync_ntp_periodically() called")
        sync_ntp()
        current_time = utime.localtime()
         
        # Calculate seconds until the top of the next hour, then add a random offset
        next_sync_secs = 3600 - current_time[5] - (60 * current_time[4]) + urandom.randint(0, 59)
        
        print(f"sync_ntp_periodically() complete. Next sync in (secs): {next_sync_secs} secs")
        await uasyncio.sleep(next_sync_secs)  # Sleep for the calculated duration