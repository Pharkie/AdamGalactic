"""
Author: Adam Knowles
Version: 0.1
Description: A digital clock with animated rolling digits (as if on a mechanical reel) that periodically syncs time
via NTP if Wifi is available, taking account of British Summer Time (BST)

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""
# Micropython libs
import utime
import urandom
import uasyncio
# import sys (only needed for sys.exit()
# Panel hardware
# My project
import config
import datetime_utils
import temp_etc_utils
import rolling_clock_display_utils
import panel_main_functions

def random_choice(probabilities):
    rand_num = urandom.randint(1, sum(probabilities))
    cumulative_prob = 0
    for i, prob in enumerate(probabilities):
        cumulative_prob += prob
        if rand_num <= cumulative_prob:
            return i

async def main():
    tasks_and_probabilities = [ # Doesn't matter if these don't add up to 100, will use relative weights
        (panel_main_functions.scroll_msg, 30),
        (panel_main_functions.rolling_clock, 30),
        (temp_etc_utils.show_temp, 30),
        (temp_etc_utils.show_humidity, 10),
        (temp_etc_utils.show_pressure, 10),
        (temp_etc_utils.show_gas, 10),
    ]
    
    current_task_index = -1  # Initialize to -1 to ensure the first task is randomly selected
    
    n = 0
    
    while True:
        n += 1
        # Randomly select a task based on probabilities, excluding the last selected task
        while True:
            new_task_index = random_choice([prob for _, prob in tasks_and_probabilities])
            if new_task_index != current_task_index:
                current_task_index = new_task_index
                break
        
        current_task, task_probability = tasks_and_probabilities[current_task_index]
        current_task_name = current_task.__name__
        current_task = loop.create_task(current_task())
        
        secs_passed = 0
        secs_target = config.CHANGE_INTERVAL + urandom.randint(0, round(config.CHANGE_INTERVAL * 0.2))
        print("Running", current_task_name, "for", secs_target, "seconds")
        
        try:
            while secs_passed < secs_target:
                await uasyncio.sleep(1)
                secs_passed += 1
        except asyncio.CancelledError:
            print("asyncio CancelledError")
            pass  # Handle the task being canceled
        
        current_task.cancel()
        
        print("Completed task", n)
        
        config.picoboard.set_pen(config.picoboard.create_pen(0, 0, 0))
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

