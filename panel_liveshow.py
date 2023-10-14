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

        panel_attract_functions.update_clock_display(values, old_values, delay=delayed_delay)

        sleep_duration = (1 + (0.8 * (i / 5) ** 2) + (0.4 * (i / 5)))

        await uasyncio.sleep(sleep_duration)

        old_values = values.copy()

async def rollback_clock_to_madness():
    # print("rolling_clock() called")
    old_values = utime.localtime(utime.mktime(utime.localtime()) + 4)

    start_time = utime.mktime(utime.localtime())

    for i in range(500):
        # Artificially alter the current time as a tuple
        fake_time = utime.localtime(start_time - i)
        values = list(datetime_utils.get_time_values(fake_time))

        if i <= 5:
            reduced_delay = 0.4 * (1 - (i / 100) ** 4)
        else:
            reduced_delay = 0.005

        panel_attract_functions.update_clock_display(values, old_values, delay=reduced_delay)

        if i <= 5:
            sleep_duration = 0.05 + (2.95 * (1 - (i / 5) ** 4))
        else:
            sleep_duration = 0.03

        await uasyncio.sleep(sleep_duration)

        old_values = values.copy()

async def main():
    # await utils.scroll_msg("Showtime")

    try:
        await uasyncio.wait_for(panel_attract_functions.rolling_clock(), timeout=4)
    except uasyncio.TimeoutError:
        print("Timed out rollback_clock() and ended")

    utils.clear_picoboard()
    uasyncio.run(advance_clock_slowly())
    uasyncio.run(rollback_clock_to_madness())

    utils.clear_picoboard()

if __name__ == "__main__":
    utils.clear_picoboard()
    datetime_utils.sync_ntp()
    uasyncio.run(main())

    # print(utime.localtime())