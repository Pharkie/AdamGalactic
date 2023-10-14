import utils
import panel_attract_functions
import uasyncio

if __name__ == "__main__":
    utils.clear_picoboard()
    uasyncio.run(panel_attract_functions.rolling_clock())