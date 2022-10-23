# esp32 project home

Host to modules I have found useful, adapted, or written and the environments I made with them for various esp32 projects.

## TODO

- read https://bhave.sh/micropython-microdot/
- separate the work done in boot.py to only the essentials (wlan connect, screen setup, essentials only), create a new main.py for the **real** work.
	- putting all that into boot.py delays the ability to connect to the esp32 serially
