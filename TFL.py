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

# line_id can be e.g. piccadilly, bakerloo, victoria
async def line_status(line_id):
    # Check if Wi-Fi is connected
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Wi-Fi is not connected")
        return []

    # Make the API request
    url = f"https://api.tfl.gov.uk/Line/{line_id}/Status"
    response = urequests.get(url)
    data = json.loads(response.text)

    # Find the status of the specified line
    line_status = None
    for line in data:
        if line["id"] == line_id:
            line_status = line["lineStatuses"][0]["statusSeverityDescription"]
            break

    if line_status is None:
        print(f"No {line_id} line status")
        return []

    print(f"{line_id} line status:", line_status)
    return line_status

# async def main(): # Test this solo
#     # Connect to Wi-Fi
#     datetime_utils.connect_wifi()

#     # Get the next bus times
#     times = await next_buses()
#     print(times)

# uasyncio.run(main())