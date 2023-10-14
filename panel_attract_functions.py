"""
Author: Adam Knowles
Version: 0.1
Description: Main functions for the panel to switch between

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import uasyncio
import utime # type: ignore
import config
import datetime_utils
import rolling_clock_display_utils

async def rolling_clock():
    # print("rolling_clock() called")
    old_values = datetime_utils.get_time_values()
        
    while True:
        start_time = utime.ticks_ms()

        # Get today's date and display it underneath the time
        current_date = utime.localtime()
        date_str = datetime_utils.format_date(current_date)
        # Set the date text color
        pen_colour_date = config.PEN_GREY
        config.picoboard.set_pen(pen_colour_date)
        config.picoboard.text(text=date_str, x1=0, y1=config.clock_digit_all_y + config.char_height + 1, wordwrap=-1, scale=1)

        values = list(datetime_utils.get_time_values())

        tick_flags = [values[i] != old_values[i] for i in range(6)]

        for i in range(6):
            for j in range(6):
                if tick_flags[j]: # Scroll that digit one row
                    # Define digit parameters as a dictionary
                    scroll_digit_params = {
                        'reverse': False,                       # Reverse flag (True or False)  
                        'top_number': old_values[j],            # Top number to display  
                        'bottom_number': values[j],             # Bottom number to display 
                        'x_pos': config.clock_digits_x[j],      # X position 
                        'y_pos': config.clock_digit_all_y,      # Y position 
                        'loop_num': i                           # Loop number  
                    }
                    rolling_clock_display_utils.scroll_digit(scroll_digit_params)
                else:
                    rolling_clock_display_utils.show_digit(old_values[j], config.clock_digits_x[j], config.clock_digit_all_y)

            pen_colour = config.PEN_YELLOW if values[5] % 2 == 0 else config.PEN_BLACK
            config.picoboard.set_pen(pen_colour)
            config.picoboard.text(text = ":", x1 = config.base_x + (2 * config.char_width), y1 = config.clock_digit_all_y, wordwrap = -1, scale = 1)
            config.picoboard.text(text = ":", x1 = config.base_x + (4 * config.char_width) + 3, y1 = config.clock_digit_all_y, wordwrap = -1, scale = 1)

            config.gu.update(config.picoboard)
            utime.sleep(0.05)

        end_time = utime.ticks_ms()
        cycle_duration = utime.ticks_diff(end_time, start_time)
        sleep_duration = 1000 - cycle_duration

        if sleep_duration > 0:
            await uasyncio.sleep_ms(sleep_duration)

        old_values = values.copy()

