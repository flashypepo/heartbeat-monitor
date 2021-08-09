# heartrate monitor - timer-based
#
# limitation: only heart rates to multiples of 60 / timer_seconds.
# Timer of 5 seconds (-> multiples of 12), the calculated heart
# rates can only be 12 (1 beat per 5 seconds), 24 (2 beats in 5 secs),
# 36 (3...), 48 (4...), 60 (5...), 72 (6...), 84, 96,108 or 120 etc.
#
# 2018-0414 WeMOS D1 mini configuration:
#           heart rate sensor: Vcc=3.3V, GND, Signal -> A0
#           built-in LED: GPIO5
# based on: https://martinfitzpatrick.name/article/wemos-heart-rate-sensor-display-micropython/
from machine import Pin, Signal, ADC, Timer
adc = ADC(0)

# On WeMOS D1 mini on = off, need to reverse.
led = Signal(Pin(2, Pin.OUT), invert=True)

MAX_HISTORY = 250

# Maintain a log of previous values to
# determine min, max and threshold.
history = []
beat = False
beats = 0

def calculate_bpm(t):
    global beats
    #print('BPM:', beats * 6) # Triggered every 10 seconds, * 6 = bpm
    print('BPM:', beats * 12) # PePo changed to triggered every 5 seconds, * 12 = bpm
    beats = 0

timer = Timer(1)
timer.init(period=5000, mode=Timer.PERIODIC, callback=calculate_bpm)

while True:
    v = adc.read()

    history.append(v)

    # Get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]

    minima, maxima = min(history), max(history)

    threshold_on = (minima + maxima * 3) // 4   # 3/4
    threshold_off = (minima + maxima) // 2      # 1/2

    if not beat and v > threshold_on:
        beat = True
        beats += 1
        led.on()

    if beat and v < threshold_off:
        beat = False
        led.off()

# PePo: when stopped (Ctrl-C): reboot device to stop Timer
