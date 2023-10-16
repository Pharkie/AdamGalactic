import datetime_utils
import utils
from time import sleep
import utime # type: ignore

if __name__ == "__main__":
    utils.clear_picoboard()
    utils.connect_wifi()
    print(f"is_DST: {datetime_utils.is_DST(utime.time())}")
    datetime_utils.sync_rtc()
    print(f"Current time tuple: {datetime_utils.get_time_values()}")
