from screen import Screen
from machine import Pin, SoftI2C
from aht20 import AHT20
from time import sleep

sda = Pin(32)
scl = Pin(33)
i2c = SoftI2C(scl, sda)

aht = AHT20(i2c)
s = Screen()
while True:
    s.clear()
    s.write('temp C: ' + str(aht.temperature), 0, 0)
    s.write('temp F: ' + str(aht.temperature_f), 0, 20)
    s.write('humidity: ' + str(aht.relative_humidity), 0, 40)
    sleep(60)
