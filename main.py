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

async def main():
    print("main() called")

    tasks = [
        (panel_attract_functions.scroll_msg, "Next stop: Penmaenmawr"),
        (temp_etc_utils.show_temp, None),
        (panel_attract_functions.next_bus_info, None),
        (panel_attract_functions.piccadilly_line_status, None),
        (temp_etc_utils.show_humidity, None),
        (temp_etc_utils.show_pressure, None),
        (temp_etc_utils.show_gas, None),
        (panel_attract_functions.rolling_clock, None),
    ]

    while True:
        # Shuffle the indices of the tasks using the Fisher-Yates shuffle algorithm
        # implemented using urandom.getrandbits(32) to generate random numbers.
        indices = list(range(len(tasks)))
        for i in range(len(tasks) - 1, 0, -1):
            j = urandom.getrandbits(32) % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        
        for i, index in enumerate(indices): # Run the tasks in the shuffled order
            task_fn, arg = tasks[index]
            current_task_name = task_fn.__name__
            current_task_probability = 100 // len(tasks)
            current_task = loop.create_task(task_fn(arg) if arg is not None else task_fn())
            
            # Allow certain tasks to complete in their own time i.e. to scroll the whole message once. Means they can execute beyond the timeout.
            if current_task_name in ["piccadilly_line_status", "next_bus_info", "scroll_msg"]: 
                print(f"Running {current_task_name} with no timeout")
                await current_task
            else:
                secs_target = config.CHANGE_INTERVAL + urandom.randint(0, round(config.CHANGE_INTERVAL * 0.2))
                print(f"Running {current_task_name} for up to {secs_target} seconds")
                
                try:
                    await uasyncio.wait_for(current_task, timeout=secs_target)
                except uasyncio.TimeoutError:
                    pass
                
                current_task.cancel()
                
                print(f"Completed task {current_task_name}")
            
            config.picoboard.set_pen(config.PEN_BLACK)
            config.picoboard.clear()
            config.gu.update(config.picoboard)

# Stop attract mode. Start the show
def stop_attract_start_show():
    print("stop_attract_start_show()")
    
    # Cancel attract tasks from global scope (we don't need "global" because we don't writing to them)
    main_task.cancel()
    sync_ntp_task.cancel()

    # Stop events in the tasks list
    for task in tasks:
        # Most of these tasks won't exist to call .cancel() on, so catch the exception and pass it
        try:
            task[0].cancel()
        except AttributeError:
            pass
    
    # Start the show
    loop.create_task(panel_liveshow.main())

# Stop the show. Start attract mode.
def stop_show_start_attract():
    print("stop_show_start_attract()") # Also starts when the show stops naturally i.e. not via a received command
    global main_task, sync_ntp_task # Let's not create new vars in this scope

    # TODO: stop the show?
    # Add the attract tasks back to the event loop, using the vars from global scope
    main_task = loop.create_task(main())
    sync_ntp_task = loop.create_task(datetime_utils.sync_ntp_periodically())

async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    print("listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
        print("listen_for_commands() checks for a command")
        command = await reader.readline()

        if command == b"show-start\n":
            stop_attract_start_show()
        elif command == b"show-stop\n":
            stop_show_start_attract()
        else:
            print("Unknown command:", command.decode().strip())
    
        await uasyncio.sleep(0.5)

if __name__ == "__main__":
    print("Start program")
    rolling_clock_display_utils.show_init_msg("PenClock", 5, 2)

    # Add tasks for the coroutines to the event loop
    loop = uasyncio.get_event_loop()

    # Tasks need to be defined here so they are accessible by both main() and stop_attract_start_show()
    tasks = [
        (panel_attract_functions.scroll_msg, "Next stop: Penmaenmawr"),
        (temp_etc_utils.show_temp, None),
        (panel_attract_functions.next_bus_info, None),
        (panel_attract_functions.piccadilly_line_status, None),
        (temp_etc_utils.show_humidity, None),
        (temp_etc_utils.show_pressure, None),
        (temp_etc_utils.show_gas, None),
        (panel_attract_functions.rolling_clock, None),
    ]

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