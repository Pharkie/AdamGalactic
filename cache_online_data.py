"""
Author: Adam Knowles
Version: 0.1
Name: cache_online_data.py
Description: A cache object that stores online data, and provides methods to set cache items and retrieve them

GitHub Repository: https://github.com/Pharkie/AdamGalactic/
License: GNU General Public License (GPL)
"""
import utime # type: ignore
import uasyncio
import config
import utils
import urequests # type: ignore
import temp_etc_utils

# Class to represent the online data cache object
class OnlineDataCache:
    def __init__(self):
        self.custom_message = None
        self.custom_message_last_updated = None
        self.piccadilly_line_status = None
        self.piccadilly_line_status_last_updated = None
        self.next_buses = None
        self.next_buses_last_updated = None
        self.cache_expiry = {
            "custom_message": None,
            "piccadilly_line_status": None,
            "next_buses": None
        }
        self.cache_expiry_times = {
            "custom_message": config.CACHE_EXPIRY_TIMES[0],
            "piccadilly_line_status": config.CACHE_EXPIRY_TIMES[1],
            "next_buses": config.CACHE_EXPIRY_TIMES[2]
        }

    # Check if a cache item is expired
    def is_expired(self, cache_item):
        return self.cache_expiry[cache_item] is not None and self.cache_expiry[cache_item] < utime.time()

    # Set the cache item with new data and expiry time
    def set(self, cache_item, data, expiry_time):
        setattr(self, cache_item, data)
        self.cache_expiry[cache_item] = expiry_time

    # Retrieve the cached item, or None if expired
    def get(self, cache_item):
        if self.is_expired(cache_item):
            return None
        else:
            return getattr(self, cache_item)
    
    async def __get_JSON_data(self, api_url):
        # print(f"__get_JSON_data() called with {api_url}")
        try:
            if not utils.is_wifi_connected():
                raise Exception("Wi-Fi is not connected")

            # Make the API request to get the data
            try:
                response = urequests.get(api_url, timeout=10)
                responseJSON = response.json()
                # Essential or we get ENOMEM errors. Don't switch for one line responseJSON = urequests.get().json()
                response.close()
            except ValueError:
                raise Exception("invalid JSON response from API")

            return responseJSON

        except Exception as e:
            raise Exception(f"Failed to get JSON data from API: {e}")

    async def update_next_buses_cache(self):
        # print("update_next_buses_cache() called")

        try:
            # Get the next bus information from the TFL API
            next_buses_data = await self.__get_JSON_data(config.next_buses_URL)

            # Extract the bus information from next_buses_data JSON
            bus_info = []
            for bus in next_buses_data:
                if bus.get("lineName") == "141":
                    time_to_station = bus["timeToStation"] // 60
                    bus_info.append(time_to_station)

            if bus_info is None:
                raise Exception("bus_info is empty")

            # Sort the times in ascending order
            bus_info.sort()

            # Set the cache with the bus information
            expiry_time = utime.time() + config.CACHE_EXPIRY_TIMES[0][1]
            self.set("next_buses", bus_info, expiry_time)
            print(f"Success. Updated next buses cache with: {bus_info}")
        except Exception as e:
            print(f"Failed to get next bus information from API: {e}")

    async def update_line_status_cache(self):
        # print("update_line_status_cache() called")

        try:
            # Get the line status data from the TFL API
            line_status_data = await self.__get_JSON_data(config.piccadilly_line_status_URL)

            # Find the status of the specified line
            line_status = None
            for line in line_status_data:
                if line["id"] == "piccadilly":
                    line_status = line["lineStatuses"][0]["statusSeverityDescription"]
                    break

            if line_status is None:
                raise Exception("could not retrieve piccadilly line status")

            # Set the cache with the line status
            expiry_time = utime.time() + config.CACHE_EXPIRY_TIMES[1][1]
            self.set("piccadilly_line_status", line_status, expiry_time)
            print(f"Success. Updated Piccadilly line status cache with: {line_status}")

        except Exception as e:
            print(f"Failed to get tube line status data from API: {e}")

    # Retrieve the custom message
    async def update_custom_message_cache(self):
        # print("update_custom_message_cache() called")

        try:
            # Get the custom message from the API
            message_info = await self.__get_JSON_data(config.custom_message_gist_URL)

            # Extract the message text from the JSON data
            message_text = message_info["custom_message"]

            if message_text is None:
                raise Exception("custom message is empty")

            # Set the cache with the message text
            expiry_time = utime.time() + config.CACHE_EXPIRY_TIMES[2][1]
            self.set("custom_message", message_text, expiry_time)
            print(f"Success. Updated custom message with: {message_text}")

        except Exception as e:
            print(f"Failed to get custom message from Gist: {e}")

    # Update each item in the cache data
    async def update_all_cache(self):
        print("update_all_cache() called")

        await uasyncio.gather(
            self.update_next_buses_cache(),
            self.update_line_status_cache(),
            self.update_custom_message_cache()
        )

        print(f"Success: all cache updated")

# Function to update the cache periodically
# async def update_cache_periodically():
#     while True:
#         await uasyncio.sleep(config.CACHE_REFRESH_INTERVAL)

#         print("\n", "=" * 100)
#         print("Updating cache post-startup (non-blocking)")
#         utils.clear_picoboard()
#         # utils.show_static_message("Syncing..", config.PEN_BLUE, 0.2)
        
#         # Show the temperature while we update the cache in the background
#         temp_etc_utils.show_temp()

#         await config.my_cache.update_all_cache()
#         print("\n", "=" * 100)
#         utils.clear_picoboard()

# Initialise
async def main():
    # print("cache_online_data.main() called")
    
    # Populate the global cache instance with a new cache object
    config.my_cache = OnlineDataCache()

    utils.clear_picoboard()
    utils.show_static_message("Syncing..", config.PEN_BLUE, 0.2)
    # temp_etc_utils.show_temp()
    print("Updating cache at startup (blocking)")
    await config.my_cache.update_all_cache()

    utils.clear_picoboard()

    # Start the update coro (moved to run in bg of static messages)
    # uasyncio.create_task(update_cache_periodically())

# If this script is run outside of a module for testing, start the update coro main(). 
# Does not run if this script is imported: main() should be run by the importer i.e. uasyncio.run(cache_online_data.main())
async def run_main_async():
    utils.connect_wifi()

    await main()

    print(f"\nNext buses gets as: {config.my_cache.get('next_buses')}")
    print(f"Line status gets as: {config.my_cache.get('piccadilly_line_status')}")
    print(f"Custom message gets as: {config.my_cache.get('custom_message')}")

if __name__ == "__main__":
    uasyncio.run(run_main_async())
