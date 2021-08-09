# main.py - select startup program
# 2018-0414 added heartrate monitor

import gc

#import scroller # OLED-demo
#import sht30_demo # SHT30 shield demo
#TODO: show temperature and humidity on OLED display

# heartrate monitor
# requires:  (requires OLED (i2c) & heartrate sensor (A0)
gc.collect() # free some memory
import heartratemonitor
heartratemonitor.detect() # go ahead
