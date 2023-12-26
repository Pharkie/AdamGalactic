import utils
import panel_attract_functions
import uasyncio
import datetime_utils

if __name__ == "__main__":
    utils.clear_picoboard()
    utils.connect_wifi()
    datetime_utils.sync_rtc()
    # uasyncio.run(panel_attract_functions.rolling_clock(3))
    uasyncio.run(panel_attract_functions.rolling_clock())