"""
Author: Adam Knowles
Version: 0.1
Name: rolling_clock_display_utils.py
Description: Utils that help display and animate the time and date

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import utime
import config

def show_digit(char_width, char_height, number_to_show, x_pos, y_pos):
    """Display a single digit at the specified position."""
    config.picoboard.set_pen(config.picoboard.create_pen(0, 0, 0)) # Can't use COLOUR_BLACK, risks a dependency loop between this and main.py
    config.picoboard.rectangle(x_pos, y_pos, char_width, char_height)
    
    config.picoboard.set_pen(config.PEN_YELLOW)
    config.picoboard.text(text = str(number_to_show), x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)
    
def scroll_digit(params):
    """Scroll one vertical row of a single digit at the specified position. Designed to be called in a loop"""
    # Unpack params dictionary
    reverse = params['reverse']
    top_number = params['top_number']
    bottom_number = params['bottom_number']
    x_pos = params['x_pos']
    y_pos = params['y_pos']
    loop_num = params['loop_num']

    # Don't know why, but this is needed
    y_pos = y_pos + 1

    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.rectangle(x_pos, y_pos, config.char_width, config.char_height)

    config.picoboard.set_clip(x_pos, y_pos, config.char_width, config.char_height)

    config.picoboard.set_pen(config.PEN_YELLOW)
    config.picoboard.text(text=str(top_number), x1=x_pos, y1=y_pos - (loop_num + 1), wordwrap=-1, scale=1)
    config.picoboard.text(text=str(bottom_number), x1=x_pos, y1=y_pos + config.char_height - (loop_num + 1), wordwrap=-1, scale=1)

    config.picoboard.remove_clip()

def show_init_msg(init_msg, x_pos, y_pos):
    """Display a message at start-up."""

    font_colour = config.PEN_BLUE
    
    config.gu.set_brightness(0.2)
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    
    config.picoboard.set_pen(font_colour)
    config.picoboard.text(text = init_msg, x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)
    config.gu.update(config.picoboard)
    config.gu.set_brightness(1.0)
    utime.sleep(0.5) # Brief name display before we get into the clock

    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.gu.update(config.picoboard)