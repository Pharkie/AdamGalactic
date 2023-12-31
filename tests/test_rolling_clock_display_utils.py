import rolling_clock_display_utils
import config
from time import sleep
import utils

def test_digit_roll(reverse_flag, oldnum, newnum):
    MY_X = 24
    MY_Y = 2

    rolling_clock_display_utils.show_digit(oldnum, MY_X, MY_Y)

    config.gu.update(config.picoboard)
    sleep(1)

    for i in range(6):
        # Define digit parameters as a dictionary
        # reverse: Reverse flag (True or False)
        # top_number: Top number to display
        # bottom_number: Bottom number to display
        # x_pos: X position
        # y_pos: Y position
        # loop_num: Loop number
        scroll_digit_params = {
            'reverse': reverse_flag,
            'old_number': oldnum,
            'new_number': newnum,
            'x_pos': MY_X,
            'y_pos': MY_Y,
            'loop_num': i
        }

        rolling_clock_display_utils.scroll_digit(scroll_digit_params)

        config.gu.update(config.picoboard)
        sleep(0.2)

    rolling_clock_display_utils.show_digit(newnum, MY_X, MY_Y)

    sleep(1)

if __name__ == "__main__":
    utils.clear_picoboard()
    test_digit_roll(False, 4, 5)
    sleep(1)
    test_digit_roll(True, 5, 4)