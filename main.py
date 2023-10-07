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
import machine
import sys
# My project
import config
import datetime_utils
import temp_etc_utils
import rolling_clock_display_utils
import panel_attract_functions
import panel_liveshow
import utils

async def main():
    print("main() called")

    # The attract_tasks list is a list of tuples, where each tuple represents a task to be run.
    # Each tuple has three elements:
    # - The first element is the function to call.
    # - The second element is an argument to pass to the function, or None if no argument is required.
    # - The third element is the timeout value in seconds, or None if the function should be run with no timeout.
    
    # Set the configurable message
    attract_tasks = [
        (panel_attract_functions.next_bus_info, None, None),
        (panel_attract_functions.piccadilly_line_status, None, None),
        (panel_attract_functions.rolling_clock, None, config.CHANGE_INTERVAL),
        (panel_attract_functions.scroll_msg, panel_attract_functions.read_configurable_message(), None),
        (temp_etc_utils.show_temp, None, config.CHANGE_INTERVAL),
        (temp_etc_utils.show_humidity, None, config.CHANGE_INTERVAL),
        (temp_etc_utils.show_pressure, None, config.CHANGE_INTERVAL),
        (temp_etc_utils.show_gas, None, config.CHANGE_INTERVAL),
    ]

    while True:
        # Shuffle the indices of the tasks using the Fisher-Yates shuffle algorithm
        # implemented using urandom.getrandbits(32) to generate random numbers.
        indices = list(range(len(attract_tasks)))
        for i in range(len(attract_tasks) - 1, 0, -1):
            j = urandom.getrandbits(32) % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]

        for i, index in enumerate(indices): # Run the tasks in the shuffled order
            task_fn, arg, timeout_secs = attract_tasks[index]
            current_task_name = task_fn.__name__

            if timeout_secs is None:
                print(f"Running {current_task_name} with no timeout")
            else:
                print(f"Running {current_task_name} for up to {timeout_secs} seconds")

            try:
                await uasyncio.wait_for(task_fn(arg) if arg is not None else task_fn(), timeout=timeout_secs)
            except uasyncio.TimeoutError:
                pass

            print(f"Completed task {current_task_name}")

            config.picoboard.set_pen(config.PEN_BLACK)
            config.picoboard.clear()
            config.gu.update(config.picoboard)

# Stop attract mode. Start the show
async def stop_attract_start_show():
    print("stop_attract_start_show()")
    
    # Cancel attract tasks from global scope (we don't need "global" because we don't writing to them)
    global main_task, sync_ntp_task
    main_task.cancel()
    sync_ntp_task.cancel()

    # Seems no need to cancel the attract tasks because they are cancelled when the main_task is cancelled
    
    # Start the show and wait for it to complete
    await panel_liveshow.main()
    
    # Start the attract mode again
    stop_show_start_attract()

# Stop the show. Start attract mode.
def stop_show_start_attract():
    print("stop_show_start_attract()") # Also starts when the show stops naturally i.e. not via a received command
    global main_task, sync_ntp_task # Let's not create new vars in this scope

    # TODO: stop the show? Not needed if the show stops naturally. Only if need a command to stop the show out of sequence.
    # Add the attract tasks back to the event loop, using the vars from global scope
    sync_ntp_task = loop.create_task(datetime_utils.sync_ntp_periodically())
    main_task = loop.create_task(main())

async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
        command = await reader.readline() # Waits for a command

        print(f"Command received: {command.decode().strip()}") 
        if command == b"show-start\n":
            await stop_attract_start_show()
        elif command == b"show-stop\n":
            stop_show_start_attract()
        else:
            print("Unknown command:", command.decode().strip())

if __name__ == "__main__":
    print("Start program")
    rolling_clock_display_utils.show_init_msg("PenClock", 5, 2)

    # Add tasks for the coroutines to the event loop
    loop = uasyncio.get_event_loop()

    utils.connect_wifi()

    # Add the attract tasks to the event loop. Creates vars that can be accessed in functions to cancel or restart.
    sync_ntp_task = loop.create_task(datetime_utils.sync_ntp_periodically())
    command_task = loop.create_task(listen_for_commands())
    main_task = loop.create_task(main())

    try:
        # Run all tasks forever
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        loop.close()