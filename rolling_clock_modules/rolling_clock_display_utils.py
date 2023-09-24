"""
Author: Adam Knowles
Version: 0.1
Name: rolling_clock_display_utils.py
Description: Utils that help display and animate the time and date

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import utime
import urandom
import uasyncio
import network
import ntptime
from machine import Timer
import sys
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

def show_digit(picoboard, font_colour, char_width, char_height, number_to_show, x_pos, y_pos):
    """Display a single digit at the specified position."""
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, char_width, char_height)
    
    pen_colour = font_colour
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = str(number_to_show), x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)
    
def scroll_digit(params):
    """Scroll a single digit at the specified position."""
    # Unpack params dictionary
    picoboard = params['picoboard']
    font_colour = params['font_colour']
    char_width = params['char_width']
    char_height = params['char_height']
    reverse = params['reverse']
    top_number = params['top_number']
    bottom_number = params['bottom_number']
    x_pos = params['x_pos']
    y_pos = params['y_pos']
    loop_num = params['loop_num']

    # Don't know why, but this is needed
    y_pos = y_pos + 1

    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, char_width, char_height)

    picoboard.set_clip(x_pos, y_pos, char_width, char_height)

    pen_colour = font_colour
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text=str(top_number), x1=x_pos, y1=y_pos - (loop_num + 1), wordwrap=-1, scale=1)
    picoboard.text(text=str(bottom_number), x1=x_pos, y1=y_pos + char_height - (loop_num + 1), wordwrap=-1, scale=1)

    picoboard.remove_clip()

def show_init_msg(picoboard, gu, font_colour, init_msg, x_pos, y_pos):
    """Display a simple message while we sync the clock on init."""
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    
    pen_colour = font_colour
    picoboard.set_pen(picoboard.create_pen(pen_colour[0], pen_colour[1], pen_colour[2]))
    picoboard.text(text = init_msg, x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)
    gu.update(picoboard)
    gu.set_brightness(1.0)
    utime.sleep(0.5) # Brief name display before we get into the clock

    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    gu.update(picoboard)
