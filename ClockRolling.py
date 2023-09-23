"""
Author: Adam Knowles
Version: 0.1
Description: A digital clock with animated rolling digits (as if on a mechanical reel) that periodically syncs time
via NTP if Wifi is available, taking account of British SUmmer Time (BST)

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
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

def is_bst(dt):
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

def show_digit(number_to_show, x_pos, y_pos):
    """Display a single digit at the specified position."""
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, char_width, char_height)
    
    pen_colour = colour_yellow
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = str(number_to_show), x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)

def scroll_digit(reverse, top_number, bottom_number, x_pos, y_pos, loop_num):
    """Scroll a single digit at the specified position."""
    # Don't know why but this is needed
    y_pos = y_pos + 1

    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, char_width, char_height)

    picoboard.set_clip(x_pos, y_pos, char_width, char_height)

    pen_colour = colour_yellow
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = str(top_number), x1 = x_pos, y1 = y_pos - (loop_num + 1), wordwrap = -1, scale = 1)
    picoboard.text(text = str(bottom_number), x1 = x_pos, y1 = y_pos + char_height - (loop_num + 1), wordwrap = -1, scale = 1)
    
    picoboard.remove_clip()

def get_time_values():
    """Get the current time and split it into individual digits."""
    global is_BST  # Access the global BST status
    
    current_time_tuple = utime.localtime()  # As set by NTP call, if Wifi is available

    # If it's BST, add an hour to the current time
    if is_BST:
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


def show_init_msg():
    """Display a simple message while we sync the clock on init."""
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    
    pen_colour = colour_blue
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = "PenClock", x1 = 5, y1 = 2, wordwrap = -1, scale = 1)
    gu.update(picoboard)
    gu.set_brightness(1.0)
    utime.sleep(0.5) # Brief name display before we get into the clock

    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    gu.update(picoboard)
    
def sync_ntp():
    global is_BST
    print('sync_ntp() called')
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    gu.update(picoboard)

    pen_colour = colour_blue
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
            print("Time set")

            # Update the global BST status
            current_time_tuple = utime.localtime()
            is_BST = is_bst(current_time_tuple)
            if is_BST:
                print("Time is BST (UTC+1), so adding an hour.")
            else:
                print("Time is not BST, so using unmodified UTC.")
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

async def sync_ntp_periodically():
    """Sync the clock at the top of the hour + 0-59 random seconds."""
    while True:
        print("sync_ntp_periodically() called")
        sync_ntp()
        current_time = utime.localtime()
        
        # Calculate the number of seconds until the next hour
        seconds_until_next_hour = 3600 - current_time[5] - (60 * current_time[4])
        
        # Add a random number of seconds between 0 and 59 (1 minute)
        next_sync_in = seconds_until_next_hour + urandom.randint(0, 59)
        
        print("Next sync in (secs): ", next_sync_in)
        await uasyncio.sleep(next_sync_in)  # Sleep for the calculated duration

async def main():
    old_values = get_time_values()
        
    while True:
        start_time = utime.ticks_ms()

        # Get today's date and display it underneath the time
        current_date = utime.localtime()
        date_str = format_date(current_date)
        # Set the date text color once
        pen_colour_date = colour_grey
        picoboard.set_pen(picoboard.create_pen(pen_colour_date[0], pen_colour_date[1], pen_colour_date[2]))
        picoboard.text(text=date_str, x1=1, y1=all_y + char_height + 1, wordwrap=-1, scale=1)

        hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones = get_time_values()
        values = [hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones]

        tick_flags = [values[i] != old_values[i] for i in range(6)]

        for i in range(6):
            for j in range(6):
                if tick_flags[j]:
                    scroll_digit(0, old_values[j], values[j], x_positions[j], all_y, i)
                else:
                    show_digit(old_values[j], x_positions[j], all_y)

            pen_colour = colour_yellow if seconds_ones % 2 == 0 else colour_black
            picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
            picoboard.text(text = ":", x1 = base_x + (2 * char_width), y1 = all_y, wordwrap = -1, scale = 1)
            picoboard.text(text = ":", x1 = base_x + (4 * char_width) + 3, y1 = all_y, wordwrap = -1, scale = 1)

            gu.update(picoboard)
            utime.sleep(0.05)

        end_time = utime.ticks_ms()
        cycle_duration = utime.ticks_diff(end_time, start_time)
        sleep_duration = 1000 - cycle_duration

        if sleep_duration > 0:
            await uasyncio.sleep_ms(sleep_duration)

        old_values = values.copy()

if __name__ == "__main__":
    # Set global variables
    gu = GalacticUnicorn()
    picoboard = PicoGraphics(DISPLAY)
    picoboard.set_font("bitmap6")
    is_BST = False
    
    colour_black = (0, 0, 0)
    colour_yellow = (255, 105, 0)
    colour_grey = (96, 96, 96)
    colour_blue = (153, 255, 255)

    base_x = 9
    char_width = 5
    char_height = 5
    
    x_positions = [base_x, base_x + 1 * char_width, base_x + (2 * char_width) + 2,
                   base_x + (3 * char_width) + 2, base_x + (4 * char_width) + 5,
                   base_x + (5 * char_width) + char_width]
    all_y = -1

    show_init_msg()


    # Add tasks for the coroutines to the event loop
    loop = uasyncio.get_event_loop()
    main_task = loop.create_task(main())
    sync_ntp_task = loop.create_task(sync_ntp_periodically())

    try:
        # Run all tasks forever
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        loop.close()


