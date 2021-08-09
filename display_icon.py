# display_icon - displays an icon on screen
# 2018-0414 PePo: 1ste version based upon heartrate monitor
# TODO: make an utility function

from machine import Pin, I2C
import ssd1306

# i2c
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def show_icon(display, icon, dx=0, dy=0):
    """display_icon(icon): dislay an icon (matrix) on display """

    for y, row in enumerate(icon):
        y += dy # offset
        for x, c in enumerate(row):
            x += dx # offset
            display.pixel(x, y, c)
    display.show()

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

# demo

# center icon on display
l = len(HEART)
w, h = 128, 32
dx = (w - l) // 2
dy = (h - l) // 2
show_icon(display, HEART, dx, dy)   # centered icon
show_icon(display, HEART)           # left-top icon
show_icon(display, HEART, 0, (h-l)) # left-bottom icon
show_icon(display, HEART, (w-l))    # right-top icon
show_icon(display, HEART, (w-l), (h-l) ) # right-bottom icon
