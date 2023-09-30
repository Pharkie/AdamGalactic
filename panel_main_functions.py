"""
Author: Adam Knowles
Version: 0.1
Description: Main functions for the panel to switch between

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import uasyncio
import utime
import config
import datetime_utils
import rolling_clock_display_utils
import TFL

async def rolling_clock():
    try:
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
                            'reverse': 0,                  # Reverse flag (0 or 1)  # type: ignore
                            'top_number': old_values[j],   # Top number to display  # type: ignore
                            'bottom_number': values[j],    # Bottom number to display  # type: ignore
                            'x_pos': config.clock_digits_x[j],                   # X position  # type: ignore
                            'y_pos': config.clock_digit_all_y,                   # Y position  # type: ignore
                            'loop_num': i                  # Loop number  # type: ignore
                        }
                        rolling_clock_display_utils.scroll_digit(scroll_digit_params)
                    else:
                        rolling_clock_display_utils.show_digit(config.char_width, config.char_height, old_values[j], config.clock_digits_x[j], config.clock_digit_all_y)

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
    except Exception as e:
        # Handle exceptions, e.g., log the error or take appropriate action
        print("Error in rolling_clock:", e)
    finally:
        # Cleanup code, if needed. Nothing to clean up?
        print("rolling_clock() complete")

async def scroll_msg():
    try:
        print("scroll_msg()")

        msg_text = "Next stop: Penmaenmawr"
        length = config.picoboard.measure_text(msg_text, 1)
        steps = length + 80 # Scroll the msg_text with a bit of padding, min 53

        while True: # Loop forever
            p = 53
            for _ in range(steps):
                config.picoboard.set_pen(config.PEN_BLACK)
                config.picoboard.clear()
                config.picoboard.set_pen(config.PEN_YELLOW)
                config.picoboard.text(text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1)  # Removed str() around msg_text
                config.gu.update(config.picoboard)
                p -= 1
                await uasyncio.sleep(0.03)
    except Exception as e:
        # Handle exceptions, e.g., log the error or take appropriate action
        print("Error in scroll_msg():", e)
    finally:
        # Cleanup code, if needed. Nothing to clean up?
        print("scroll_msg() complete")

async def next_bus_info():
    try:
        print("next_bus()")

        next_bus_times = await TFL.next_buses()
        times_str = ", ".join(next_bus_times)
        msg_text = f"Next 141 in: {times_str} mins"

        length = config.picoboard.measure_text(msg_text, 1)
        steps = length + 53 # Scroll the msg_text with a bit of padding, min 53

        while True: # Loop forever
            p = 53
            for _ in range(steps):
                config.picoboard.set_pen(config.PEN_BLACK)
                config.picoboard.clear()
                config.picoboard.set_pen(config.PEN_YELLOW)
                config.picoboard.text(text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1)
                config.gu.update(config.picoboard)
                p -= 1
                await uasyncio.sleep(0.03)
    except Exception as e:
        # Handle exceptions, e.g., log the error or take appropriate action
        print("Error in next_bus():", e)
    finally:
        # Cleanup code, if needed. Nothing to clean up?
        print("next_bus() complete")