import utils
import panel_attract_functions
import uasyncio
import datetime_utils

if __name__ == "__main__":
    utils.clear_picoboard()
    datetime_utils.sync_ntp()
    uasyncio.run(panel_attract_functions.rolling_clock())