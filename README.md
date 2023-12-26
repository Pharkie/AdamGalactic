# AdamGalactic

Adam's Galactic Unicorn LED display. A hobby project the cycles between various information displays on the LED panel, with online features, in a reasonably robust way.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Installation

1. Clone or fork from Github. 
2. Upload files to your Galactic Unicorn. Suggest use "Upload Project" from [MicroPico Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go).
3. Create a text file "wifi_creds.py" in the root dir/ with the following contents:
```
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PASSWORD = "<YOUR WIFI PASSWORD>"
```
4. Set config options in config.py
5. Run main.py.
6. Profit.

## Usage

Set the things you want to run in the "attract_tasks" tuple in main.py, and set how long to run each task in config.py.

To start the **live show**, open a separate Terminal and send (Mac example). Replace `/dev/cu.usbmodem144101` with the serial device of the Galactic Unicorn on your system, which might be a COM port on Windows,
```
echo "show-start" > /dev/cu.usbmodem144101
```

## Features

Attract mode: a series of time-bound functions that cycle between them. Functions:
- Rolling clock, a custom clock with a "mechanical rolling" animation between digits rather than just turn on/off. Also shows today's date.
- Show a custom string from a Gist, online.
- Show temperature, humidity, pressure & gas from Bosch BME680 connected via QT
- Show the next bus at a local stop (via London UK TFL API). 
- Show the status of the Piccadilly tube line (also via TFL API).
  
- Attract mode and Live show. Trigger the panel out of attract mode into the live show by sending a command ("show-start") via serial port.
- Clock (RTC on board) syncs via NTP over wifi at start-up and just after the top of each hour

**Online Data Cache**

Gets three online data items and stores them in a Cache object:
1. Next buses from a given bus stop, from TFL API
2. Piccadilly Line (tube) status,  from TFL API
3. Contents of a JSON file online from a Github Gist to set a custom message to scroll

Each of the three is retrieved at startup while the display shows "Syncing.."
Once retrieved, each of these is set with an expiry in seconds, after which they will not be used.
The cache for each is updated during the display of a different static text message. It does it this way, because updating during a scrolling or animated message causes a glitch. The glitch is because the call out to the API is blocking and takes a few seconds to retrieve the online data in each case. Couldn't find a way around this, because the [non-blocking http client for Micropython, aiohttp](https://github.com/micropython/micropython-lib/tree/master/micropython/uaiohttpclient) does not allow https:// requests (only http://). So, since the cache updates is going to block for a few seconds every minute, I hid the update in the background behind static text displays.
This is all handled by cache_online_data.py, which has a Class with getters and setters to do what I need.

## Contributing

Thank you for considering contributing to my project! I welcome contributions from everyone, regardless of their level of experience or expertise.

Please, follow these guidelines:

1. Fork the repository and create your branch from main.
2. Make your changes and ensure that they work as expected.
3. Write tests for your changes and ensure that they pass.
4. Submit a pull request with your changes.
5. I will review your pull request or provide feedback. Please be patient. This is a hobby project and it may take time for me to review your changes.

If you find a bug or have a feature request, please open an issue on my GitHub repository. I welcome feedback and suggestions, and I will do my best to address any issues.

## Credits

Galatic Unicorn hardware and software stack is awesome and created by [Pimoroni in Sheffield, UK](https://shop.pimoroni.com/).

## License

GNU General Public License (GPL)

The GPL is a free software license that allows users to run, study, modify, and distribute the software. The GPL requires that **any modified or derived versions of the software be released under the same license**, which helps to ensure that the software remains free and open source. If you use or distribute this software, you may need to include a copy of the GPL with your distribution and comply with its terms.