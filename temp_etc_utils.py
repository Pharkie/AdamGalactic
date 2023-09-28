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
    config.picoboard.set_pen(config.COLOUR_BLACK)
    config.picoboard.clear()
    config.picoboard.set_pen(config.COLOUR_GREY)
    
    # Calculate the X position to center the text horizontally
    text_width = config.picoboard.measure_text(msg, 1)
    x_pos = (53 - text_width) // 2
    
    config.picoboard.text(text=msg, x1=x_pos, y1=2, wordwrap=-1, scale=1)
    config.gu.update(config.picoboard)
    
    await uasyncio.sleep(50) # Task will be cut short elsewhere

async def show_temp():
    print("show_temp()")
    
    temperature_reading, _, _, _, status_reading, _, _ = config.bme.read()
    
     # heater = "Stable" if status_reading & STATUS_HEATER_STABLE else "Unstable" # Use this somehow? Don't show temp unless stable?
    
    msg_text = "Temp: {:.0f}c".format(round(temperature_reading))
    
    await display_static_message(msg_text)

async def show_pressure():
    print("show_pressure()")
    
    _, pressure_reading, _, _, _, _, _ = config.bme.read()
    
    msg_text = "Press: {:.0f} hPa".format(round(pressure_reading))
    
    await display_static_message(msg_text)

async def show_humidity():
    print("show_humidity()")
    
    _, _, humidity_reading, _, _, _, _ = config.bme.read()
    
    msg_text = "Hum: {:.0f}%".format(round(humidity_reading))
    
    await display_static_message(msg_text)

async def show_gas():
    print("show_gas()")
    
    _, _, _, gas_reading, _, _, _ = config.bme.read()
    
    msg_text = "Gas: {} Ohms".format(round(gas_reading))
    
    await display_static_message(msg_text)
