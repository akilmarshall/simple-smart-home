from screen import Screen
from time import sleep
import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface

s = Screen()
# while True:
s.clear()
s.write('wlan:' + wlan.isconnected(), 0, 0)
# sleep(5)
