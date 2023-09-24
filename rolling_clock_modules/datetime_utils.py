"""
Author: Adam Knowles
Version: 0.1
Name: datetime_utils.py
Description: Utils that operate on datetime

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import utime
import urandom
import uasyncio
import network
import ntptime
from machine import Timer
import sys
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

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
    
def get_time_values(BST_active):
    """Get the current time and split it into individual digits."""
    current_time_tuple = utime.localtime()  # As set by NTP call, if Wifi is available

    # If it's BST, add an hour to the current time
    if BST_active:
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

def sync_ntp(picoboard, gu, font_colour):
    """Turn on wifi, sync RTC to NTP, turn wifi off, return BST_active True or False."""
    
    print('sync_ntp() called')
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    gu.update(picoboard)

    pen_colour = font_colour
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = "Syncing..", x1 = 5, y1 = 2, wordwrap = -1, scale = 1)
    gu.update(picoboard)
    gu.set_brightness(1.0)

    try:
        from secrets import WIFI_SSID, WIFI_PASSWORD
    except ImportError:
        print("Create secrets.py with your WiFi credentials to get time from NTP")
        return

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for Wifi to connect')
        utime.sleep(0.3) # This is not using async because we need to block the clock from display updates until the sync is complete

    if max_wait > 0:
        print("Connected")

        try:
            ntptime.settime() # No parameters available for DST offset
            print("Time set from NTP")

            # Update the global BST status
            current_time_tuple = utime.localtime()
            BST_active = check_BST_active(current_time_tuple);
        except OSError:
            print("Failed to set time")
            pass
    else:
        print("Timed out waiting for Wifi")

    wlan.disconnect()
    wlan.active(False)
    
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    gu.update(picoboard)
    
    if BST_active:
        print("BST (UTC+1) set to True.")
    else:
        print("BST set to False.")
    
    return BST_active
