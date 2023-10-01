"""
Author: Adam Knowles
Version: 0.1
Description: Run the live show on the panel

GitHub Repository: https://github.com/Pharkie/AdamGalactic/ClockRolling.py
License: GNU General Public License (GPL)
"""

import uasyncio
import utime
import config
import panel_attract_functions

async def main():
    await panel_attract_functions.scroll_msg("Show start")