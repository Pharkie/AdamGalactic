"""
Author: Adam Knowles
Version: 0.1
Name: utils.py
Description: General utils not specific to a particular thing

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import config
import network
import utime

import uasyncio

def clear_picoboard():
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.gu.update(config.picoboard)

def show_static_message(message, pen_colour, x, y, brightness=1.0):
    current_brightness = config.gu.get_brightness()
    config.gu.set_brightness(brightness)
    config.picoboard.set_pen(pen_colour)
    config.picoboard.text(text=message, x1=x, y1=y, wordwrap=-1, scale=1)
    config.gu.update(config.picoboard)
    config.gu.set_brightness(current_brightness)

async def scroll_msg(msg_text):
    print(f"scroll_msg() called with msg_text: {msg_text}")

    length = config.picoboard.measure_text(msg_text, 1)
    steps = length + 53 # Scroll the msg_text with a bit of padding, min 53

    p = 53
    for _ in range(steps):
        config.picoboard.set_pen(config.PEN_BLACK)
        config.picoboard.clear()
        config.picoboard.set_pen(config.PEN_YELLOW)
        config.picoboard.text(text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1)
        config.gu.update(config.picoboard)
        p -= 1
        await uasyncio.sleep(0.03)

    print("scroll_msg() complete")

async def scroll_configured_message():
    # Retrieve the msg from the cache
    msg = config.my_cache.get("configurable_message")
    print(f"scroll_configured_message() called to scroll {msg}")
    
    # Get configurable message from cache, if available
    try:
        # Check if msg is None (i.e. expired)
        if msg is None:
            raise Exception("Error: msg is expired or missing")

        # Scroll the msg
        print(f"Scrolling msg: {msg}")
        await scroll_msg(msg)

    except Exception as e:
        print(f"Error: {e}")

def connect_wifi():
    print("connect_wifi() called")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs # type: ignore
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD) # type: ignore

    clear_picoboard()

    show_static_message("Hi, wifi?", config.PEN_BLUE, 5, 2, 0.2)

    # Wait for connect success or failure
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for Wifi to connect")
        # Doesn't use async await to block the clock from display updates until the sync is complete
        utime.sleep(0.3)

    if max_wait > 0:
        print("Wifi connected")
    else:
        print("Wifi not connected: timed out")

    clear_picoboard()
    
def is_wifi_connected():
    is_it = network.WLAN(network.STA_IF).isconnected()
    print(f"is_wifi_connected() called and returns {is_it}")
    return is_it

def disconnect_wifi():
    print("disconnect_wifi() called")
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)