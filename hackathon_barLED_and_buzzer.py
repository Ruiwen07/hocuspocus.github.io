from machine import Pin
import utime
from time import sleep

# Working is working time
# Treat counts down from 3 and dispenses candy
# Break is break time
# --> Break is determined by length of working time

pin = [6,7,8,9,10,11,12,13,14,15]
led = []

buzzer = Pin(4, Pin.OUT)
buzzer.low()

motor1A = Pin(2, Pin.OUT)
motor1A.value(1)

timerLength = 20 # * 60 Minutes
treat = 10 # Seconds
breakTimer = timerLength/5 # Minutes

#Setting led to led pins
for i in range(10):
    led.append(None)
    led[i] = Pin(pin[i], Pin.OUT)
    
def dispense_treat(seconds):
    motor1A.value(0)
    sleep(seconds)
    motor1A.value(1)
    
def flash_lights():
    for i in range(3):
        led.value(1)
        utime.sleep(0.5)
        led.value(0)
        utime.sleep(0.5)

def working(timerLength):
    for i in range(10):
        led[i].toggle()
        utime.sleep(timerLength/10)

print("Working...")
working(timerLength)
print("Candy incoming!!")
flash_lights()
print("Dispensing :)")
dispense_treat(0.1)
print("Break Time!")

