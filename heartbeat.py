# heartbeat sensor reading - detecting a beat
# 2018-0414 PePo 1ste version from
# https://martinfitzpatrick.name/article/wemos-heart-rate-sensor-display-micropython/
from machine import Pin, Signal, ADC

# create a Led object
led = Signal(Pin(2, Pin.OUT), invert=True)
led.off() # led off

# history of measurement
MAX_HISTORY = 250
history=[]

while True:
    # read the sensor value
    v = adc.read()
    # and append to history
    history.append(v)

    # get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]

    minima, maxima =  min(history), max(history)

    threshold_on = (minima + maxima * 3) // 4 # 3/4
    threshold_off = (minima + maxima) // 2  # 1/2

    if v > threshold_on:
        led.on()
    if v < threshold_off:
        led.off()
