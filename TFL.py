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
import config
# import uasyncio # Just for testing solo
# import datetime_utils # Just for testing solo

async def next_buses_list():
    # Check if Wi-Fi is connected
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        raise Exception("wifi not connected")
    
    # Make the API request
    response = urequests.get(url=config.next_buses_URL, timeout=5)

    if not response.status_code == 200:
        raise Exception(f"expected status 200, got {response.status_code}")
    
    data = json.loads(response.text)
    times = []
    for bus in data:
        if bus.get("lineName") == "141":
            time_to_station = bus["timeToStation"] // 60
            times.append(time_to_station)

    # Sort the times in ascending order
    times.sort()

    response.close()

    if times is None:
        raise Exception(f"No arrivals found for {stop_id}")
    else:
        # Replace 0 with "due"
        times_str = ["due" if time == 0 else str(time) for time in times]

        print(f"next_buses_list() returning: {times_str}")

        return times_str

# line_id can be e.g. piccadilly, bakerloo, victoria
async def line_status():
    # Check if Wi-Fi is connected
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        raise Exception("wifi not connected")

    # Make the API request
    response = urequests.get(config.piccadilly_line_status_URL, timeout=5)

    if not response.status_code == 200:
        raise Exception(f"expected status 200, got {response.status_code}")
    
    data = json.loads(response.text)
    response.close()

    # Find the status of the specified line
    line_status = None
    for line in data:
        if line["id"] == "piccadilly":
            line_status = line["lineStatuses"][0]["statusSeverityDescription"]
            break

    if line_status is None:
        raise Exception("No piccadilly line status")

    print(f"Returning piccadilly line status:", line_status)
    return line_status

# async def main(): # Test this solo
#     # Connect to Wi-Fi
#     datetime_utils.connect_wifi()

#     # Get the next bus times
#     times = await next_buses()
#     print(times)

# uasyncio.run(main())