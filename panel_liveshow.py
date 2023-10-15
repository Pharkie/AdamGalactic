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

async def advance_clock_slowly():
    # print("rolling_clock() called")
    old_values = datetime_utils.get_time_values()

    real_time = utime.mktime(utime.localtime())

    for i in range(5):
        # Artificially alter the current time as a tuple
        fake_time = utime.localtime(real_time + i)
        values = list(datetime_utils.get_time_values(fake_time))

        delayed_delay = 0.05 + (0.35 * (i / 5) ** 2)

        panel_attract_functions.update_clock_display(values, old_values, delay=delayed_delay, reverse=False)

        sleep_duration = (1 + (0.8 * (i / 5) ** 2) + (0.4 * (i / 5)))

        await uasyncio.sleep(sleep_duration)

        old_values = values.copy()

def cubic_bezier(t, p0, p1, p2, p3):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

def exponential_acceleration(x):
    return int(1.15 ** x)

async def rollback_clock_to_madness():
    # print("rolling_clock() called")
    start_time = utime.time()
    duration = 10
    subtract_secs = 0
    counter = 0

    while utime.time() - start_time < duration:
        t = (utime.time() - start_time) / duration
        reduced_delay = cubic_bezier(t, 0.04, 0.001, 0.0001, 0)
        sleep_duration = cubic_bezier(t, 0.7, 0.001, 0.0001, 0)

        # Artificially alter the current time as a tuple
        fake_time = utime.localtime(start_time - subtract_secs)
        values = list(datetime_utils.get_time_values(fake_time))

        # Initiliase old_values on the first loop to be the same as values
        if subtract_secs == 0:
            old_values = values.copy()

        panel_attract_functions.update_clock_display(values, old_values, delay=reduced_delay, reverse=True)

        await uasyncio.sleep(sleep_duration)

        old_values = values.copy()

        subtract_secs += exponential_acceleration(counter)
        # i += int(cubic_bezier(t, 1, 1.1, 100, 10000))
        counter += 1
        print(f"subtract_secs = {subtract_secs}")

async def main():
    # await utils.scroll_msg("Showtime")

    try:
        await uasyncio.wait_for(panel_attract_functions.rolling_clock(), timeout=4)
    except uasyncio.TimeoutError:
        print("Timed out rollback_clock() and ended")

    utils.clear_picoboard()
    # uasyncio.run(advance_clock_slowly())
    uasyncio.run(rollback_clock_to_madness())

    utils.clear_picoboard()

if __name__ == "__main__":
    utils.clear_picoboard()
    datetime_utils.sync_ntp()
    uasyncio.run(main())

    # print(utime.localtime())