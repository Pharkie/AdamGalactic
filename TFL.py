"""
Author: Adam Knowles
Version: 0.1
Name: TFL.py
Description: Functions to interface with TFL API for transport info

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import network
import urequests
import json
# import uasyncio # Just for testing solo
# import datetime_utils # Just for testing solo

async def next_buses():
    # Check if Wi-Fi is connected
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Wi-Fi is not connected")
        return []
    
    # Make the API request
    url = "https://api-nile.tfl.gov.uk/StopPoint/490008766S/Arrivals"
    response = urequests.get(url)
    data = json.loads(response.text)
    times = []
    for bus in data:
        if bus.get("lineName") == "141":
            time_to_station = bus["timeToStation"] // 60
            times.append(time_to_station)

    # Sort the times in ascending order
    times.sort()
    print("Next buses in", times)

    # Replace 0 with "due"
    times_str = ["due" if time == 0 else str(time) for time in times]

    return times_str

# async def main(): # Way to test this solo
#     # Connect to Wi-Fi
#     datetime_utils.connect_wifi()

#     # Get the next bus times
#     times = await next_buses()
#     print(times)

# uasyncio.run(main())