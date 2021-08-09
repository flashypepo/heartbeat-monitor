# heartrate monitor - the demo version - icon, bpm, graphics
#
# 2018-0414 WeMOS D1 mini configuration:
#           heart rate sensor: Vcc=3.3V, GND, Signal -> A0
#           OLED: SDA=GPIO5/D1, SCL=GPIO4/D2, Vcc=3.3V, GND, 128*32 pixels
#
# based on: https://martinfitzpatrick.name/article/wemos-heart-rate-sensor-display-micropython/
from machine import Pin, Signal, I2C, ADC, Timer
import ssd1306
import time

# sensor
adc = ADC(0)

# i2c
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

MAX_HISTORY = 200
TOTAL_BEATS = 30

# heart image for display on the OLED screen.
# 1-color screen: set each pixel to either on 1 or off 0.
HEART = [
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 1, 1, 1, 1, 0, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 0, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

# In the refresh block we first scroll the display left,
# for the rolling trace meter. We scroll the whole display
# because there is no support for region scroll in framebuf.
# The other areas of the display are wiped clear anyway,
# so it has no effect on appearance.
# If we have data we plot the trace line, scaled automatically
# to the min and max values for the current window.
# Finally we write the BPM to the display, along with the heart icon
# if we're currently in a beat state.
last_y = 0

def refresh(bpm, beat, v, minima, maxima):
    global last_y

    display.vline(0, 0, 32, 0)
    display.scroll(-1,0) # Scroll left 1 pixel

    if maxima-minima > 0:
        # Draw beat line.
        y = 32 - int(16 * (v-minima) / (maxima-minima))
        display.line(125, last_y, 126, y, 1)
        last_y = y

    # Clear top text area.
    display.fill_rect(0,0,128,16,0) # Clear the top text area

    if bpm:
        display.text("%d bpm" % bpm, 12, 0)

    # Draw heart if beating.
    if beat:
        for y, row in enumerate(HEART):
            for x, c in enumerate(row):
                display.pixel(x, y, c)

    display.show()

# The BPM calculation uses the beats queue, which contains the timestamp
# (in seconds) of each detected beat. By comparing the time at
# the beginning and the end of the queue we get a total time duration.
# The number of values in the list equals the number of beats detected.
# By dividing the number by the duration we get beats/second
# (*60 for beats per minute).
def calculate_bpm(beats):
    if beats:
        beat_time = beats[-1] - beats[0]
        if beat_time:
            return (len(beats) / (beat_time)) * 60

# In the main detection loop we read the sensor,
# calculate the on and off thresholds and
# then test our value agains these.
# We recalculate BPM on each beat, and refresh the screen on each loop.
# Depending on the speed of your display you may want to update
# less regularly.
def detect():
    # Maintain a log of previous values to
    # determine min, max and threshold.
    history = []
    beats = []
    beat = False
    bpm = None

    # Clear screen to start.
    display.fill(0)
    # 2018-0414 PePo added startup screen
    display.text("Heartrate", 0, 0)
    display.text("PePo 2018", 0, 16)
    display.show()
    time.sleep(5.0) # show it
    display.fill(0) # clear screen
    # endof added code

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
            # Truncate beats queue to max
            beats = beats[-TOTAL_BEATS:]
            bpm = calculate_bpm(beats)

        if v < threshold_off and beat == True:
            beat = False

        refresh(bpm, beat, v, minima, maxima)

# execute
if "__name__" == "__main__":
    detect()
