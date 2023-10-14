"""
Author: Adam Knowles
Version: 0.1
Name: rolling_clock_display_utils.py
Description: Utils that help display and animate the time and date

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import config
import utils
from time import sleep # Just for testing

def show_digit(number_to_show, x_pos, y_pos):
    """Display a single digit at the specified position."""
    config.picoboard.set_pen(config.picoboard.create_pen(0, 0, 0)) # Can't use COLOUR_BLACK, risks a dependency loop between this and main.py
    config.picoboard.rectangle(x_pos, y_pos, config.char_width, config.char_height)
    
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

if __name__ == "__main__":
    utils.clear_picoboard()

    TOPNUM = 7
    BTMNUM = 8
    MY_X = 24
    MY_Y = 2

    show_digit(TOPNUM, MY_X, MY_Y)
    config.gu.update(config.picoboard)
    sleep(1)
    
    for i in range(6):
        # Define digit parameters as a dictionary
        scroll_digit_params = {
            'reverse': False,                   # Reverse flag (0 or 1)
            'top_number': TOPNUM,                    # Top number to display
            'bottom_number': BTMNUM,                 # Bottom number to display
            'x_pos': MY_X,                        # X position
            'y_pos': MY_Y,  # Y position
            'loop_num': i                       # Loop number
        }
        
        scroll_digit(scroll_digit_params)

        config.gu.update(config.picoboard)
        sleep(0.05)

    show_digit(BTMNUM, MY_X, MY_Y)
    sleep(1)

    utils.clear_picoboard()