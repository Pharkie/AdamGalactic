"""
Author: Adam Knowles
Version: 0.1
Name: TFL.py
Description: Functions to interface with TFL API for transport info

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import uasyncio
import config
from utils import scroll_msg

async def scroll_next_bus_info():
    print("scroll_next_bus_info() called")
    
    # Get next buses from cache, if available
    try:
        # Retrieve the next_buses data from the cache
        next_buses_data = config.my_cache.get("next_buses")

        # Check if the next_buses data is None (i.e. expired)
        if next_buses_data is None:
            raise Exception("Error: next_buses data is expired or missing")
        else:
            if not next_buses_data:
                raise Exception(f"No arrivals found for given bus stop")
            else:
                # Replace 0 with "due"
                bus_info_str = ["due" if time == 0 else str(time) for time in next_buses_data]
                bus_info_str = ", ".join(bus_info_str)

                # Scroll the bus information
                print(f"Next 141: {bus_info_str} mins")
                await scroll_msg(f"Next 141: {bus_info_str} mins")

    except Exception as e:
        print("Error:", e)

async def scroll_piccadilly_line_status():
    print("scroll_piccadilly_line_status() called")

    # Get line status from cache, if available
    try:
        # Retrieve the line status data from the cache
        line_status = config.my_cache.get("piccadilly_line_status")

        # Check if the line status data is None (i.e. expired)
        if line_status is None:
            raise Exception("Error: line status data is expired or missing")
        
        # Scroll the line status information
        print(f"Scrolling Piccadilly line status: {line_status}")
        await scroll_msg(f"Piccadilly line: {line_status}")

    except Exception as e:
        print("Error:", e)