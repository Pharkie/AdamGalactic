import utils
import panel_attract_functions
import uasyncio
import datetime_utils
import utime # type: ignore

async def rollback_clock_test():
    # print("rolling_clock() called")
    old_values = datetime_utils.get_time_values()

    real_time = utime.mktime(utime.localtime())

    for i in range(5):
        # Artificially alter the current time as a tuple
        fake_time = utime.localtime(real_time - i)
        # print(f"fake_time: {real_time - i}; real_time: {real_time}")
        new_values = list(datetime_utils.get_time_values(fake_time))
        # print(f"values: {new_values} old_values: {old_values}")
        panel_attract_functions.update_clock_display(new_values, old_values, delay=0.05, reverse=True)

        await uasyncio.sleep(0.7)

        old_values = new_values.copy()

if __name__ == "__main__":
    utils.clear_picoboard()
    datetime_utils.sync_rtc()
    uasyncio.run(rollback_clock_test())