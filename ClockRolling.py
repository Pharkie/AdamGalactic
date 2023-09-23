import utime
import urandom
import uasyncio
import network
import ntptime
from machine import Timer
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

def show_digit(display_number, x_pos, y_pos):
    """Display a single digit at the specified position."""
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, 5, 6)
    
    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(display_number), x_pos, y_pos, -1, scale=1)

def scroll_digit(reverse, top_number, bottom_number, x_pos, y_pos, loop_num):
    """Scroll a single digit at the specified position."""
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.rectangle(x_pos, y_pos, 5, 6)
    
    picoboard.set_clip(x_pos, y_pos, 5, 6)

    picoboard.set_pen(picoboard.create_pen(255, 105, 0))
    picoboard.text(str(top_number), x_pos, y_pos - 1 - loop_num, -1, scale=1)
    picoboard.text(str(bottom_number), x_pos, y_pos + 5 - loop_num, -1, scale=1)
    
    picoboard.remove_clip()

def get_time_values():
    """Get the current time and split it into individual digits."""
    current_time = utime.localtime() # Uses microcontroller's internal clock, which may be unreliable
    hours_tens, hours_ones = divmod(current_time[3], 10)
    minutes_tens, minutes_ones = divmod(current_time[4], 10)
    seconds_tens, seconds_ones = divmod(current_time[5], 10)
    return hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones

def show_init_msg():
    """Display a simple message while we sync the clock on init."""
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    
    picoboard.set_pen(picoboard.create_pen(153, 255, 255))
    picoboard.text("PenClock", 5, 2, -1, scale=1)
    gu.update(picoboard)
    gu.set_brightness(1.0)
    
def sync_ntp():
    print('sync_ntp() called')
    gu.set_brightness(0.2)
    picoboard.set_pen(picoboard.create_pen(0, 0, 0))
    picoboard.clear()
    
    picoboard.set_pen(picoboard.create_pen(0, 204, 0))
    picoboard.text("Syncing..", 5, 2, -1, scale=1)
    gu.update(picoboard)
    gu.set_brightness(1.0)
    
    try:
        from secrets import WIFI_SSID, WIFI_PASSWORD
    except ImportError:
        print("Create secrets.py with your WiFi credentials to get time from NTP")
        return

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for Wifi to connect')
        utime.sleep(0.3) # This is not using async because we need to block the clock from display updates until the sync is complete

    if max_wait > 0:
        print("Connected")

        try:
            ntptime.settime()
            print("Time set")
        except OSError:
            print("Failed to set time")
            pass
    else:
        print("Timed out waiting for Wifi")

    wlan.disconnect()
    wlan.active(False)
    
async def sync_ntp_periodically():
    while True:
        print("sync_ntp_periodically() called")
        sync_ntp()
#        next_sync_in = 60 * 60 + urandom.randint(0, 59) # Live mode
        next_sync_in = urandom.randint(6, 12) # Dev mode
        print("Next sync in (secs): ", next_sync_in)
        await uasyncio.sleep(next_sync_in)  # Sleep for a random duration between 60 and 61 minutes

async def main():
    # Create a GalacticUnicorn object and initialize graphics
    picoboard.set_font("bitmap6")
    
    old_values = get_time_values()
    
    base_x = 10
    char_width = 5
    x_positions = [base_x, base_x + 1 * char_width, base_x + (2 * char_width) + 2,
                   base_x + (3 * char_width) + 2, base_x + (4 * char_width) + 5,
                   base_x + (5 * char_width) + char_width]
    all_y = -1
    
    while True:
        start_time = utime.ticks_ms()
    
        hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones = get_time_values()
        values = [hours_tens, hours_ones, minutes_tens, minutes_ones, seconds_tens, seconds_ones]
    
        tick_flags = [values[i] != old_values[i] for i in range(6)]
        
        picoboard.set_pen(picoboard.create_pen(0, 0, 0))
        picoboard.clear()
    
        for i in range(6):
            for j in range(6):
                if tick_flags[j]:
                    scroll_digit(0, old_values[j], values[j], x_positions[j], all_y, i)
                else:
                    show_digit(old_values[j], x_positions[j], all_y)
    
            if seconds_ones % 2 == 0:
                picoboard.set_pen(picoboard.create_pen(255, 105, 0))
                picoboard.text(":", base_x + (2 * char_width), all_y, -1, 0.5)
                picoboard.text(":", base_x + (4 * char_width) + 3, all_y, -1, 0.5)
    
            gu.update(picoboard)
            await uasyncio.sleep(0.05)
    
        end_time = utime.ticks_ms()
        cycle_duration = utime.ticks_diff(end_time, start_time)
        sleep_duration = 1000 - cycle_duration
    
        if sleep_duration > 0:
            await uasyncio.sleep_ms(sleep_duration)
    
        old_values = values.copy()

if __name__ == "__main__":
    gu = GalacticUnicorn()
    picoboard = PicoGraphics(DISPLAY)

    show_init_msg()
    utime.sleep(0.5) # Brief name display before we get into the clock

    # Create an event loop
    loop = uasyncio.get_event_loop()

    # Create tasks for the coroutines
    sync_ntp_task = loop.create_task(sync_ntp_periodically())
    main_task = loop.create_task(main())

    try:
        # Run the main coroutine
        loop.run_until_complete(main_task)
        # Start the periodic NTP synchronization
        loop.run_until_complete(sync_ntp_task)
    except KeyboardInterrupt:
        pass
    finally:
        # Close the event loop
        loop.close()

