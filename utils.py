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

def connect_wifi():
    """Connect to Wi-Fi and return True if successful, False otherwise."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs # type: ignore
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD) # type: ignore

    config.gu.set_brightness(0.2)
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.gu.update(config.picoboard)

    config.picoboard.set_pen(config.PEN_BLUE)
    config.picoboard.text(text = "Hi, wifi?", x1 = 5, y1 = 2, wordwrap = -1, scale = 1)
    config.gu.update(config.picoboard)
    config.gu.set_brightness(1.0)

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
        return True
    else:
        print("Wifi not connected: timed out")
        return False

def disconnect_wifi():
    """Disconnect from Wi-Fi."""

    print('disconnect_wifi() called')
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)
