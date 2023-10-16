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

def show_digit(number_to_show, x_pos, y_pos):
    """Display a single digit at the specified position."""
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.rectangle(x_pos, y_pos, config.char_width, config.char_height)
    
    config.picoboard.set_pen(config.PEN_YELLOW)
    config.picoboard.text(text = str(number_to_show), x1 = x_pos, y1 = y_pos, wordwrap = -1, scale = 1)
    
def scroll_digit(params):
    # Scroll one vertical row of a single digit at the specified position. 
    # Call in a 6 x loop (loop_num 0 to 5), once for each vertical row of pixels

    # Unpack params dictionary
    reverse = params['reverse']
    old_number = params['old_number']
    new_number = params['new_number']
    x_pos = params['x_pos']
    y_pos = params['y_pos']
    loop_num = params['loop_num']

    if reverse:
        loop_num = 5 - loop_num

    # Don't know why, but this is needed
    y_pos = y_pos + 1

    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.rectangle(x_pos, y_pos, config.char_width, config.char_height)

    config.picoboard.set_clip(x_pos, y_pos, config.char_width, config.char_height)
    config.picoboard.set_pen(config.PEN_YELLOW)

    if not reverse:
        top_number_y = y_pos - (loop_num + 1)
        bottom_number_y = y_pos + config.char_height - (loop_num + 1)
        # print(f"reverse False. Loop: {loop_num}, top_number_y {top_number_y}, bottom_number_y {bottom_number_y}")

        config.picoboard.text(text=str(old_number), x1=x_pos, y1=top_number_y, wordwrap=False, scale=1)
        config.picoboard.text(text=str(new_number), x1=x_pos, y1=bottom_number_y, wordwrap=False, scale=1)
    else:
        loop_num = config.char_height - loop_num - 1

        top_number_y = y_pos - config.char_height + loop_num
        bottom_number_y = y_pos + loop_num

        # print(f"reverse True. Loop: {loop_num}, top_number_y {top_number_y}, bottom_number_y {bottom_number_y}")

        config.picoboard.text(text=str(new_number), x1=x_pos, y1=top_number_y, wordwrap=False, scale=1)
        config.picoboard.text(text=str(old_number), x1=x_pos, y1=bottom_number_y, wordwrap=False, scale=1)

    config.picoboard.remove_clip()