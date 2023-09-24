"""
Author: Adam Knowles
Version: 0.1
Description: A digital clock with animated rolling digits (as if on a mechanical reel) that periodically syncs time
via NTP if Wifi is available, taking account of British Summer Time (BST)

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import utime
import urandom
import uasyncio
# import sys (only needed for sys.exit()
from rolling_clock_modules import datetime_utils
from rolling_clock_modules import rolling_clock_display_utils
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

async def sync_ntp_periodically():
    """Sync the clock at the top of the hour + 0-59 random seconds."""
    
    global BST_active # Need to set this
    
    while True:
        print("sync_ntp_periodically() called")
        BST_active = datetime_utils.sync_ntp(picoboard, gu, colour_blue)
        current_time = utime.localtime()
        
        # Calculate the number of seconds until the next hour
        seconds_until_next_hour = 3600 - current_time[5] - (60 * current_time[4])
        
        # Add a random number of seconds between 0 and 59 (1 minute)
        next_sync_in = seconds_until_next_hour + urandom.randint(0, 59)
        
        print("Next sync in (secs): ", next_sync_in)
        await uasyncio.sleep(next_sync_in)  # Sleep for the calculated duration

async def main():
    old_values = datetime_utils.get_time_values(BST_active)
        
    while True:
        start_time = utime.ticks_ms()

        # Get today's date and display it underneath the time
        current_date = utime.localtime()
        date_str = datetime_utils.format_date(current_date)
        # Set the date text color
        pen_colour_date = colour_grey
        picoboard.set_pen(picoboard.create_pen(pen_colour_date[0], pen_colour_date[1], pen_colour_date[2]))
        picoboard.text(text=date_str, x1=0, y1=all_y + char_height + 1, wordwrap=-1, scale=1)

        values = list(datetime_utils.get_time_values(BST_active))

        tick_flags = [values[i] != old_values[i] for i in range(6)]

        for i in range(6):
            for j in range(6):
                if tick_flags[j]: # Scroll that digit one row
                    # Define digit parameters as a dictionary
                    scroll_digit_params = {
                        'picoboard': picoboard,         # Your picoboard instance
                        'font_colour': colour_yellow,  # Font color
                        'char_width': char_width,      # Character width
                        'char_height': char_height,    # Character height
                        'reverse': 0,                  # Reverse flag (0 or 1)
                        'top_number': old_values[j],   # Top number to display
                        'bottom_number': values[j],    # Bottom number to display
                        'x_pos': x_positions[j],                   # X position
                        'y_pos': all_y,                   # Y position
                        'loop_num': i                  # Loop number
                    }
                    rolling_clock_display_utils.scroll_digit(scroll_digit_params)
                else:
                    rolling_clock_display_utils.show_digit(picoboard, colour_yellow, char_width, char_height, old_values[j], x_positions[j], all_y)

            pen_colour = colour_yellow if values[5] % 2 == 0 else colour_black
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
    BST_active = False
    
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

    rolling_clock_display_utils.show_init_msg(picoboard, gu, colour_blue, "PenClock", 5, 2)

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


