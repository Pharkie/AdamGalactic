import utime
import math
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Constants for controlling scrolling text
MESSAGE_COLOUR = (255, 105, 0)
BACKGROUND_COLOUR = (0, 0, 0)
BOTTOM_TEXT = "20 Sep 2023"

# Create a GalacticUnicorn object
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# Set font e.g. bitmap6, bitmap8, sans
graphics.set_font("bitmap6")

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

gu.set_brightness(1)

def freeze_time():
    print("here")
    # Get the current time in HH:MM:SS format
    current_time = utime.localtime()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    
    # Update the TOP_TEXT variable
    TOP_TEXT = formatted_time

    graphics.set_pen(graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
    graphics.clear()

    graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
    graphics.text(TOP_TEXT, 10, -1, -1, 0.4)
    graphics.text(BOTTOM_TEXT, 0, 5, -1, 0.4)
    
    # Update the display
    gu.update(graphics)

while True:
    # Get the current time in HH:MM:SS format
    current_time = utime.localtime()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    
    # Update the TOP_TEXT variable
    TOP_TEXT = formatted_time

    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        gu.adjust_brightness(+0.01)

    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        freeze_time()
        break

    graphics.set_pen(graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
    graphics.clear()

    graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
    graphics.text(TOP_TEXT, 10, -1, -1, 0.4)
    graphics.text(BOTTOM_TEXT, 0, 5, -1, 0.4)
    
    # Update the display
    gu.update(graphics)

    # Pause for a moment (important or the USB serial device may fail)
    utime.sleep(0.1)  # Adjust the sleep duration to 0.5 seconds for a faster colon flash

