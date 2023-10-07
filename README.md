# AdamGalactic
Adam's Galactic Unicorn LED display (hardware and software stack by Pimoroni in Sheffield, UK)

A hobby project that features:

Attract mode: a series of time-bound functions that cycle between them. Current functions:
- Rolling clock, a custom clock with a "mechanical rolling" animation between digits rather than just turn on/off. Also shows today's date.
- Show temperature, humidity, pressure & gas from Bosch BME680 connected via QT
- Show a user configured string. 
- Show the next bus at a local stop (via London UK TFL API). 
- Show the status of the Piccadilly tube line (also via TFL API).
  
Attract mode and Live show. Trigger out of attract mode into the live show by sending a command via serial port.
Clock (RTC on board) syncs via NTP over wifi at start-up and just after the top of the hour
