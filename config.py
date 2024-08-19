"""
Author: Adam Knowles
Version: 0.1
Name: config.py
Description: Set up global config, variables and objects

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

from galactic import GalacticUnicorn  # type: ignore
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY  # type: ignore
from pimoroni_i2c import PimoroniI2C  # type: ignore
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE, FILTER_COEFF_3, STANDBY_TIME_1000_MS, OVERSAMPLING_16X, OVERSAMPLING_2X, OVERSAMPLING_1X  # type: ignore

# GU stuff
gu = GalacticUnicorn()
picoboard = PicoGraphics(DISPLAY)

DISPLAY_WIDTH = 53

# Pen colours
PEN_BLACK = picoboard.create_pen(0, 0, 0)
PEN_YELLOW = picoboard.create_pen(255, 105, 0)
PEN_GREY = picoboard.create_pen(96, 96, 96)
PEN_BLUE = picoboard.create_pen(153, 255, 255)
PEN_GREEN = picoboard.create_pen(38, 133, 40)

picoboard.set_font("bitmap6")

# BME680 stuff
BME_ENABLED = False
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}  # type: ignore

if BME_ENABLED:
    i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
    bme = BreakoutBME68X(
        i2c
    )  # Declare once. If you put this in a function and keep calling it, it will crash the panel after a while. # type: ignore
    # Configure the BME680. These are defaults anyway, but here in case I want to change them later
    bme.configure(FILTER_COEFF_3, STANDBY_TIME_1000_MS, OVERSAMPLING_16X, OVERSAMPLING_2X, OVERSAMPLING_1X)  # type: ignore

# Other stuff
from wifi_creds import WIFI_SSID, WIFI_PASSWORD

CHANGE_INTERVAL = 6  # seconds

base_x = 9
char_width = 5
char_height = 5

clock_digits_x = [
    base_x,
    base_x + 1 * char_width,
    base_x + (2 * char_width) + 2,
    base_x + (3 * char_width) + 2,
    base_x + (4 * char_width) + 5,
    base_x + (5 * char_width) + char_width,
]
clock_digit_all_y = -1

custom_message_gist_URL = "https://gist.githubusercontent.com/Pharkie/b411446bb13e8d9c73500d09b66862a2/raw/CustomMessage.txt"
next_buses_URL = "https://api.tfl.gov.uk/Line/141/Arrivals/490008766S"
piccadilly_line_status_URL = "https://api.tfl.gov.uk/Line/piccadilly/Status"

DEFAULT_CUSTOM_MESSAGE = "Next stop: Penmaenmawr"

# Make a global instance of the cache object, so it can be used by multiple modules.
# Variable is populated in cache_online_data.main()
my_cache = None  # type: ignore

CACHE_REFRESH_INTERVAL = 60  # seconds

CACHE_EXPIRY_TIMES = (
    ("next_buses", 1 * 60),  # 1 minutes
    ("line_status", 5 * 60),  # 10 minutes
    ("custom_message", 60 * 60),  # 60 minutes
)
