from random import random

F = 80
HUM = 85

def fake_temp():
    global F
    F += random() * 2
    return F

def fake_hum():
    global HUM
    HUM += random() * 2
    return HUM
