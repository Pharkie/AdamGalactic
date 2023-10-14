import temp_etc_utils
import utils
from time import sleep

if __name__ == "__main__":
    utils.clear_picoboard()
    temp_etc_utils.show_temp()
    sleep(2)
    temp_etc_utils.show_pressure()
    sleep(2)
    temp_etc_utils.show_humidity()
    sleep(2)
    temp_etc_utils.show_gas()
    sleep(2)
    utils.clear_picoboard()