from secrets import psk, ssid
from time import sleep

import network
from screen import Screen


s = Screen()  # setup the screen

# Setup the WLAN
wlan = network.WLAN(network.STA_IF)
s.write('bringing up the', 0, 0)
s.write('wlan interface', 0, 20)
wlan.active(True)
for i in range(4):
    s.write('.', i * 3, 40) 
    sleep(0.5)

wlan.connect(ssid, psk)
while True:
    status = wlan.status()
    s.clear()
    if status == network.STAT_IDLE:
        s.write('no connection', 0, 0)
        s.write('and no activity', 0, 20)
    elif status == network.STAT_CONNECTING:
        s.write('connection in', 0, 0)
        s.write('progress', 0, 20)
    elif status == network.STAT_WRONG_PASSWORD:
        s.write('wrong psk', 0, 0)
    elif status == network.STAT_NO_AP_FOUND:
        s.write('no ssid found', 0, 0)
    elif status == network.STAT_CONNECT_FAIL:
        s.write('failed', 0, 0)
    elif status == network.STAT_GOT_IP:
        s.write('got IP', 0, 0)
    for i in range(4):
        s.write('.', i * 3, 40) 
        sleep(0.5)
    if wlan.isconnected():
        break

def write_web_info():
    s.clear()
    s.write(wlan.ifconfig()[0], 0, 0)

write_web_info()
import main
