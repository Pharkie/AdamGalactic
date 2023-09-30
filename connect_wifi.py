"""
Author: Adam Knowles
Version: 0.1
Name: connect_wifi.py
Description: Connect Pico W to Wifi so can then use e.g. mip.install('micropython-requests') to install a lib

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import network
import mip

WIFI_SSID = "MooseCave"
WIFI_PASSWORD = "This7Muggles2%"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print(wlan.isconnected())