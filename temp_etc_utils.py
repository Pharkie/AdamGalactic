"""
Author: Adam Knowles
Version: 0.1
Description: Utils for BME680

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import config
import utils
import uasyncio


def show_temp():
    # print("show_temp()")
    if not config.BME_ENABLED:
        return "No BME"

    temperature_reading, _, _, _, status_reading, _, _ = config.bme.read()

    # heater = "Stable" if status_reading & STATUS_HEATER_STABLE else "Unstable" # Use this somehow? Don't show temp unless stable?

    msg_text = "Temp: {:.0f}c".format(round(temperature_reading), chr(176))

    utils.show_static_message(msg_text, config.PEN_GREY, 1.0)

    return msg_text


async def show_temp_coro():
    show_temp()

    await uasyncio.sleep(20)


def show_pressure():
    # print("show_pressure()")

    if not config.BME_ENABLED:
        return "No BME"

    _, pressure_reading, _, _, _, _, _ = config.bme.read()

    msg_text = "Pressure: {:.0f} hPa".format(round(pressure_reading / 100))

    utils.show_static_message(msg_text, config.PEN_GREY, 1.0)

    return msg_text


async def show_pressure_coro():
    show_pressure()

    await uasyncio.sleep(20)


def show_humidity():
    # print("show_humidity()")

    if not config.BME_ENABLED:
        return "No BME"

    _, _, humidity_reading, _, _, _, _ = config.bme.read()

    msg_text = "Humidity: {:.0f}%".format(round(humidity_reading))

    utils.show_static_message(msg_text, config.PEN_GREY, 1.0)

    return msg_text


async def show_humidity_coro():
    show_humidity()

    await uasyncio.sleep(20)


def show_gas():
    # print("show_gas()")

    if not config.BME_ENABLED:
        return "No BME"

    _, _, _, gas_reading, _, _, _ = config.bme.read()

    msg_text = "Gas: {} kOhms".format(round(gas_reading / 1000))

    utils.show_static_message(msg_text, config.PEN_GREY, 1.0)

    return msg_text


async def show_gas_coro():
    show_gas()

    await uasyncio.sleep(20)
