"""
Author: Adam Knowles
Version: 0.1
Description: Utils for BME680

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""
import config
import uasyncio

async def display_static_message(msg):
    config.picoboard.set_pen(config.PEN_BLACK)
    config.picoboard.clear()
    config.picoboard.set_pen(config.PEN_GREY)
    
    # Calculate the X position to center the text horizontally
    text_width = config.picoboard.measure_text(msg, 1)
    x_pos = (53 - text_width) // 2
    
    # Split the message into two lines if the text width is greater than 53
    if text_width > 53:
        # Find the index of the space closest to the center of the message
        space_index = len(msg) // 2
        while msg[space_index] != ' ':
            space_index += 1
        
        # Split the message into two lines at the space index
        line1 = msg[:space_index]
        line2 = msg[space_index+1:]
        
        # Calculate the X position to center each line horizontally
        text_width1 = config.picoboard.measure_text(line1, 1)
        x_pos1 = (53 - text_width1) // 2
        text_width2 = config.picoboard.measure_text(line2, 1)
        x_pos2 = (53 - text_width2) // 2
        
        # Display each line of the message on a separate line
        config.picoboard.text(text=line1, x1=x_pos1, y1=-1, wordwrap=-1, scale=1)
        config.picoboard.text(text=line2, x1=x_pos2, y1=5, wordwrap=-1, scale=1)
    else:
        # Display the message on a single line
        config.picoboard.text(text=msg, x1=x_pos, y1=2, wordwrap=-1, scale=1)
    
    config.gu.update(config.picoboard)
    
    await uasyncio.sleep(50) # Task will be cut short elsewhere

async def show_temp():
    print("show_temp()")
    
    temperature_reading, _, _, _, status_reading, _, _ = config.bme.read()
    
     # heater = "Stable" if status_reading & STATUS_HEATER_STABLE else "Unstable" # Use this somehow? Don't show temp unless stable?
    
    msg_text = "Temp: {:.0f}c".format(round(temperature_reading),chr(176))
    
    await display_static_message(msg_text)

async def show_pressure():
    print("show_pressure()")
    
    _, pressure_reading, _, _, _, _, _ = config.bme.read()
    
    msg_text = "Pressure: {:.0f} hPa".format(round(pressure_reading / 100))
    
    await display_static_message(msg_text)

async def show_humidity():
    print("show_humidity()")
    
    _, _, humidity_reading, _, _, _, _ = config.bme.read()
    
    msg_text = "Humidity: {:.0f}%".format(round(humidity_reading))
    
    await display_static_message(msg_text)

async def show_gas():
    print("show_gas()")
    
    _, _, _, gas_reading, _, _, _ = config.bme.read()
    
    msg_text = "Gas: {} kOhms".format(round(gas_reading / 1000))
    
    await display_static_message(msg_text)