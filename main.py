"""
Author: Adam Knowles
Version: 0.1
Description: A digital clock with animated rolling digits (as if on a mechanical reel) that periodically syncs time
via NTP if Wifi is available, taking account of British Summer Time (BST)

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""
# Micropython libs
import urandom # type: ignore
import TFL
import uasyncio
import sys
# My project
import config
import datetime_utils
import temp_etc_utils
import panel_attract_functions
import panel_liveshow
import utils
import cache_online_data

async def show_temp_and_update_next_buses_cache():
    await uasyncio.gather(temp_etc_utils.show_temp_coro(), config.my_cache.update_next_buses_cache())

async def show_humidity_and_update_line_status_cache():
    await uasyncio.gather(temp_etc_utils.show_humidity_coro(), config.my_cache.update_line_status_cache())

async def show_pressure_and_update_custom_message_cache():
    await uasyncio.gather(temp_etc_utils.show_pressure_coro(), config.my_cache.update_custom_message_cache())

async def run_attract_mode():
    # print("run_attract_mode() called")
    
    global my_cache

    # List of tasks to be run, each represented by a tuple with a function to call and a timeout value.
    # Updates different parts of the cache in the background while displaying some of the static messages.
    # Params: (function name, timeout_secs)
    attract_tasks = [
        (TFL.scroll_next_bus_info, None),
        (TFL.scroll_piccadilly_line_status, None),
        (utils.scroll_configured_message, None),
        (panel_attract_functions.rolling_clock, config.CHANGE_INTERVAL),
        (show_temp_and_update_next_buses_cache, config.CHANGE_INTERVAL),
        (show_humidity_and_update_line_status_cache, config.CHANGE_INTERVAL),
        (show_pressure_and_update_custom_message_cache, config.CHANGE_INTERVAL),
        (temp_etc_utils.show_gas_coro, config.CHANGE_INTERVAL),
    ]

    # last_index to ensure that the first task of the current loop is not the same as the last task of the previous loop i.e. runs twice in a row
    last_index = None
    while True:
        # Shuffle the indices of the tasks using the Fisher-Yates shuffle algorithm
        # implemented using urandom.getrandbits(32) to generate random numbers.
        indices = list(range(len(attract_tasks)))
        for i in range(len(attract_tasks) - 1, 0, -1):
            j = urandom.getrandbits(32) % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]

        # Check if the first item of the current loop is the same as the last item of the previous loop
        if last_index is not None and indices[0] == last_index:
            middle_index = len(indices) // 2
            # Swap first task with middle task if necessary
            indices[0], indices[middle_index] = indices[middle_index], indices[0]

        for i, index in enumerate(indices): # Run the tasks in the shuffled order
            task_fn, timeout_secs = attract_tasks[index]
            
            # if timeout_secs is None:
            #     print(f"Running {task_fn.__name__} with no timeout")
            # else:
            #     print(f"Running {task_fn.__name__} for up to {timeout_secs} seconds")

            try:
                await uasyncio.wait_for(task_fn() if timeout_secs is None else task_fn(), timeout=timeout_secs)
            except uasyncio.TimeoutError:
                pass

            # print(f"Completed task {current_task_name}")

            config.picoboard.set_pen(config.PEN_BLACK)
            config.picoboard.clear()
            config.gu.update(config.picoboard)

        # Store the last index for the next loop
        last_index = indices[-1]

        # await uasyncio.sleep(5) # Debugging

# Stop attract mode. Start the show
async def stop_attract_start_show():
    print("stop_attract_start_show()")
    
    # Cancel attract tasks from global scope (we don't need "global" because we don't writing to them)
    # (Seems no need to cancel the attract tasks because they are cancelled when the main_task is cancelled)
    global attract_mode_task, sync_ntp_task
    attract_mode_task.cancel()
    sync_ntp_task.cancel()

    # Start the show and wait for it to complete
    await panel_liveshow.main()
    
    # Start the attract mode again
    stop_show_start_attract()

# Stop the show. Start attract mode.
def stop_show_start_attract():
    # print("stop_show_start_attract()") # Also starts when the show stops naturally i.e. not via a received command
    global attract_mode_task, sync_ntp_task # Let's not create new vars in this scope

    # TODO: stop the show? Not needed if the show stops naturally. Only if need a command to stop the show out of sequence.
    # Add the attract tasks back to the event loop, using the vars from global scope
    sync_ntp_task = uasyncio.create_task(datetime_utils.sync_ntp_periodically())
    attract_mode_task = uasyncio.create_task(run_attract_mode())

async def listen_for_commands():
    # Uses the uasyncio.StreamReader class to read input from the standard input asynchronously without blocking.
    # print("listen_for_commands() started")
    reader = uasyncio.StreamReader(sys.stdin)

    while True:
        if config.gu.is_pressed(config.GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            config.gu.adjust_brightness(+0.01)
            config.gu.update(config.picoboard)
            await uasyncio.sleep(0.01)

        if config.gu.is_pressed(config.GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            config.gu.adjust_brightness(-0.01)
            config.gu.update(config.picoboard)
            await uasyncio.sleep(0.01)

        # Waits for a command and blocks the rest of this function, so need for sleep in this loop
        command = await reader.readline() 

        print(f"Command received: {command.decode().strip()}") 
        if command == b"show-start\n":
            await stop_attract_start_show()
        elif command == b"show-stop\n":
            stop_show_start_attract()
        else:
            print("Unknown command:", command.decode().strip())

if __name__ == "__main__":
    print("Start program")
    utils.show_static_message("PenClock", config.PEN_BLUE, 0.2)

    utils.connect_wifi()
    # Update the online data cache at startup
    uasyncio.run(cache_online_data.main())

    # Add the attract tasks to the event loop. Creates vars that can be accessed in functions to cancel or restart.
    sync_ntp_task = uasyncio.create_task(datetime_utils.sync_ntp_periodically())
    command_task = uasyncio.create_task(listen_for_commands())
    attract_mode_task = uasyncio.create_task(run_attract_mode())

    try:
        uasyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        uasyncio.get_event_loop().close()