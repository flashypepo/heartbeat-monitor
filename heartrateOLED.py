# heartrate monitor, BPM on OLED SSD1306 128 * 32 pixels
# 2018-0414 WeMOS D1 mini configuration:
#           heart rate sensor: Vcc=3.3V, GND, Signal -> A0
#           built-in LED: GPIO5
#           OLED: SDA=GPIO5/D1, SCL=GPIO4/D2, Vcc=3.3V, GND
# based upon: https://martinfitzpatrick.name/article/wemos-heart-rate-sensor-display-micropython/
from machine import Pin, Signal, ADC, Timer, I2C
import ssd1306
import time

# sensor
adc = ADC(0)

# OLED display
i2c = I2C(-1, scl=Pin(5), sda=Pin(4)) # PePo changed: added keywords
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# On WeMOS D1 mini on = off, need to reverse.
led = Signal(Pin(2, Pin.OUT), invert=True)

MAX_HISTORY = 250
TOTAL_BEATS = 30

def calculate_bpm(beats):
    beats = beats[-TOTAL_BEATS:]
    beat_time = beats[-1] - beats[0]
    if beat_time:
        bpm = (len(beats) / (beat_time)) * 60
        display.fill(0) # PePo added: clear display
        display.text("%d bpm" % bpm, 12, 0)
        display.show() # PePo added: show buffer onscreen

def detect():
    history = []
    beats = []
    beat = False

    while True:
        v = adc.read()

        history.append(v)

        # Get the tail, up to MAX_HISTORY length
        history = history[-MAX_HISTORY:]

        minima, maxima = min(history), max(history)

        threshold_on = (minima + maxima * 3) // 4   # 3/4
        threshold_off = (minima + maxima) // 2      # 1/2

        if v > threshold_on and beat == False:
            beat = True
            beats.append(time.time())
            beats = beats[-TOTAL_BEATS:]
            calculate_bpm(beats)
            led.on()  # PePo aded LED

        if v < threshold_off and beat == True:
            beat = False
            led.off() # PePo aded LED

# PePo added: execute
detect()
