from time import sleep
import temp_etc_utils
import utils
import config

if __name__ == "__main__":
    utils.clear_picoboard()

    if not config.BME_ENABLED:
        print("No BME")
    else:
        temp_etc_utils.show_temp()
        sleep(2)
        temp_etc_utils.show_pressure()
        sleep(2)
        temp_etc_utils.show_humidity()
        sleep(2)
        temp_etc_utils.show_gas()
        sleep(2)
        utils.clear_picoboard()
