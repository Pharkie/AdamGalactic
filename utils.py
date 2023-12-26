"""
Author: Adam Knowles
Version: 0.1
Name: utils.py
Description: General utils not specific to a particular thing

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""

import config
import network # type: ignore
import utime # type: ignore

import uasyncio

def clear_picoboard():
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.gu.update(config.picoboard)

def show_static_message(message, pen_colour, brightness=1.0):
    # print(f"show_static_message() called with message: {message}, pen_colour: {pen_colour}, brightness: {brightness}")

    previous_brightness = config.gu.get_brightness()
    clear_picoboard()

    config.picoboard.set_pen(config.PEN_GREY)
    
    # Calculate the X position to center the text horizontally
    text_width = config.picoboard.measure_text(message, 1)
    x_pos = (config.DISPLAY_WIDTH - text_width) // 2
    
    # Split the message into two lines if the text width is greater than display width
    if text_width > config.DISPLAY_WIDTH:
        # Find the index of the space closest to the center of the message
        space_index = len(message) // 2
        while message[space_index] != ' ':
            space_index += 1
        
        # Split the message into two lines at the space index
        line1 = message[:space_index]
        line2 = message[space_index+1:]
        
        # Calculate the X position to center each line horizontally
        text_width1 = config.picoboard.measure_text(line1, 1)
        x_pos1 = (config.DISPLAY_WIDTH - text_width1) // 2
        text_width2 = config.picoboard.measure_text(line2, 1)
        x_pos2 = (config.DISPLAY_WIDTH - text_width2) // 2
        
        # Display each line of the message on a separate line
        config.picoboard.text(text=line1, x1=x_pos1, y1=-1, wordwrap=-1, scale=1)
        config.picoboard.text(text=line2, x1=x_pos2, y1=5, wordwrap=-1, scale=1)
    else:
        # Display the message on a single line
        config.picoboard.text(text=message, x1=x_pos, y1=2, wordwrap=-1, scale=1)
    
    config.gu.set_brightness(brightness)
    config.gu.update(config.picoboard)
    config.gu.set_brightness(previous_brightness)

async def scroll_msg(msg_text):
    # print(f"scroll_msg() called with msg_text: {msg_text}")

    length = config.picoboard.measure_text(msg_text, 1)
    steps = length + config.DISPLAY_WIDTH # Scroll the msg_text with a bit of padding, min 53

    p = config.DISPLAY_WIDTH
    for _ in range(steps):
        config.picoboard.set_pen(config.PEN_BLACK)
        config.picoboard.clear()
        config.picoboard.set_pen(config.PEN_YELLOW)
        config.picoboard.text(text=msg_text, x1=p, y1=2, wordwrap=-1, scale=1)
        config.gu.update(config.picoboard)
        p -= 1
        await uasyncio.sleep(0.03)

    # print("scroll_msg() complete")

async def scroll_configured_message():
    # Retrieve the msg from the cache
    msg = config.my_cache.get("custom_message")
    # print(f"scroll_configured_message()")
    
    # Get custom message from cache, if available
    try:
        # Check if msg is None (i.e. expired)
        if msg is None:
            raise Exception("Error: msg is expired or missing")

        await scroll_msg(msg)

    except Exception as e:
        print(f"Error: {e}")

def connect_wifi():
    # print("connect_wifi() called")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs # type: ignore
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD) # type: ignore

    clear_picoboard()

    show_static_message("Hi, wifi?", config.PEN_BLUE, 0.2)

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
    # print(f"is_wifi_connected() called and returns {is_it}")
    return is_it

def disconnect_wifi():
    # print("disconnect_wifi() called")
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)