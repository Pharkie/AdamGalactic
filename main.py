"""
Author: Adam Knowles
Version: 0.1
Description: A digital clock with animated rolling digits (as if on a mechanical reel) that periodically syncs time
via NTP if Wifi is available, taking account of British Summer Time (BST)

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""
# Micropython libs
import urandom
import uasyncio
# My project
import config
import datetime_utils
import temp_etc_utils
import rolling_clock_display_utils
import panel_main_functions

async def main():
    tasks = [
        panel_main_functions.scroll_msg,
        temp_etc_utils.show_temp,
        panel_main_functions.next_bus_info,
        temp_etc_utils.show_humidity,
        temp_etc_utils.show_pressure,
        temp_etc_utils.show_gas,
    ]
    
    while True:
        # Shuffle the indices of the tasks using the Fisher-Yates shuffle algorithm
        # implemented using urandom.getrandbits(32) to generate random numbers.
        indices = list(range(len(tasks)))
        for i in range(len(tasks) - 1, 0, -1):
            j = urandom.getrandbits(32) % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        
        for i, index in enumerate(indices): # Run the tasks in the shuffled order
            current_task = tasks[index] if i % 2 == 0 else panel_main_functions.rolling_clock
            current_task_name = current_task.__name__
            current_task_probability = 100 // len(tasks)
            current_task = loop.create_task(current_task())
            
            secs_target = config.CHANGE_INTERVAL + urandom.randint(0, round(config.CHANGE_INTERVAL * 0.2))
            print("Running", current_task_name, "for", secs_target, "seconds")
            
            await uasyncio.sleep(secs_target)
            
            current_task.cancel()
            
            print("Completed task", current_task_name)
        
            config.picoboard.set_pen(config.PEN_BLACK)
            config.picoboard.clear()
            config.gu.update(config.picoboard)


if __name__ == "__main__":

    rolling_clock_display_utils.show_init_msg("PenClock", 5, 2)

    # Add tasks for the coroutines to the event loop
    loop = uasyncio.get_event_loop()
    main_task = loop.create_task(main())
    sync_ntp_task = loop.create_task(datetime_utils.sync_ntp_periodically())

    try:
        # Run all tasks forever
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        loop.close()
