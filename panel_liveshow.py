"""
Author: Adam Knowles
Version: 0.1
Description: Run the live show on the panel

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import uasyncio
import utime # type: ignore
import config
import utils
import datetime_utils
import panel_attract_functions

async def advance_clock_slowly(old_values):
    # print("rolling_clock() called")
    # old_values = datetime_utils.get_time_values()

    real_time = utime.mktime(utime.localtime())
    sleep_duration = 0

    for i in range(3):
        # Artificially alter the current time as a tuple
        fake_time_tuple = utime.localtime(real_time + i)
        new_values = list(datetime_utils.get_time_values(fake_time_tuple))

        delayed_delay = 0.05 * pow(2, i)

        panel_attract_functions.update_clock_display(new_values, old_values, delay=delayed_delay, reverse=False)

        # Exponential acceleration
        sleep_duration = 1 * pow(1.25, i)

        await uasyncio.sleep(sleep_duration)

        old_values = new_values.copy()
    
    return fake_time_tuple

async def rollback_clock_to_madness(fake_start_time_tuple):
    # print("rollback_clock_to_madness() called")
    # print(f"fake_start_time_tuple: {fake_start_time_tuple}")

    start_time = utime.mktime(fake_start_time_tuple)

    duration = 10
    subtract_secs = 0
    counter = 0

    while utime.time() - start_time < duration:
        delay = 0.2 * pow(0.6, counter)
        sleep_duration = 1 * pow(0.6, counter)

        # Artificially alter the current time as a tuple
        fake_time_tuple = utime.localtime(start_time - subtract_secs)
        new_values = list(datetime_utils.get_time_values(fake_time_tuple))

        # Initiliase old_values on the first loop to be the same as values
        if counter == 0:
            old_values = new_values.copy()
            delay = 0
            sleep_duration = 0

        # print(f"counter {counter} delay {delay} sleep_duration = {sleep_duration} subtract_secs {subtract_secs}")

        panel_attract_functions.update_clock_display(new_values, old_values, delay=delay, reverse=True)

        await uasyncio.sleep(sleep_duration)

        old_values = new_values.copy()

        # Exponential acceleration
        subtract_secs += int(1 * pow(1.25, counter))
        counter += 1

async def main():
    # await utils.scroll_msg("Showtime")

    time_tuple_at_end = uasyncio.run(panel_attract_functions.rolling_clock(4))
    # print(f"time_tuple_at_end: {time_tuple_at_end}")
    fake_time_tuple_at_end = uasyncio.run(advance_clock_slowly(time_tuple_at_end))
    uasyncio.run(rollback_clock_to_madness(fake_time_tuple_at_end))

    utils.clear_picoboard()

if __name__ == "__main__":
    utils.clear_picoboard()
    datetime_utils.sync_ntp()
    uasyncio.run(main())

    # print(utime.localtime())