#tsync quick test UK
from time import sleep
import TSYNC
from utime import localtime, mktime, gmtime
from machine import RTC, deepsleep
import network
import sys

def connect(station):
    station.active(True)
    station.config(reconnects = 5)
    count = 0
    station.connect(ssid,password)
    while not station.isconnected():
        print('.', end="")
        sleep(1)
        count += 1
        if count > 30: break          
    if station.isconnected():
        print('WLAN connection to ' + ssid + ' succeeded!')
        return True
    else:
        print('Unable to make connection after ' + str(count) + ' tries.')
        return False

#Change ssid and password to your credentials to obtain internet connection
ssid = 'Gigaclear_F9D0'
password = 'y7rq0aez88'

rtc = RTC()    
station = network.WLAN(network.STA_IF)
station.active(False)
"""
UTILITY FOR TESTING TSYNC.py NORTHERN HEMISPHERE
TSYNC parameters: zone, locale, separator, year_format, country, hemisphere
locale:
The desired date format: should be 1 to 3
1 = dd-mm-yyyy
2 = mm-dd-yyyy
3 = yyyy-mm-dd

separator: 0 for a hyphen, 1 for a slash.
year_format: 0 for 4 digit year, 1 for 2 digit year

Hemisphere: True for North, False for South.
"""
year = 2024
#You may change this, but if you do you must also change
#all the spring and autumn dates below accordingly.

#set rtc with UTC time using  GPS
#(year,month,mday,hour,minute,second,0,0)
gps_tuple = (year,1,1,10,0,0,0,0) #Any date in January 

print('\n\n')
"""Uncomment the country you want to test. 
START FROM POWER ON RESET, NOT SOFT RESET"""

#initialise library with debug on for verbose reporting
clk = TSYNC.TimeSync(0,1,0,0,'EU',True) #EU
#clk = TSYNC.TimeSync(-8,1,0,0,'USA',True,True) #USA and Canada
#clk = TSYNC.TimeSync(2,1,0,0,'EG',True,True) #Egypt
#clk = TSYNC.TimeSync(0,1,0,0,'USER',True,True) #User

spring = (2024,3,31, 2, 0,0,0,0) #EU
#spring = (2024,3,29, 2, 1,59,55,0) #USA
#spring = (2024,4,26, 0, 10,59,55,0) #EG
#spring = (2024,4,31, 0, 1,59,55,0) #USER
print('Set time 2am, March 31 UTC')
clk.debug = True
print('Timestamp now is ' + clk.set_GPS_time(spring) + '\n')
print('Advance to Autumn.....\n')
print('Set time 2am Oct 27, UTC')
autumn = (2024,10,27, 2, 0,0,0,0) #EU
#autumn = (2025,11,10, 2, 0,59,55,0) #USA
#autumn = (2025,10,31, 10, 0,59,55,0) #EG
#autumn = (2024,10,27, 0, 0,59,55,0) #USER
print('Timestamp now is ' + clk.set_GPS_time(autumn) + '\n')
spring = (2025,3,30, 2, 0,0,0,0) #EU
#spring = (2025,3,31, 0, 1,59,55,0) #USA
#spring = (2025,4,27, 0, 10,59,55,0) #EG
#spring = (2025,3,31, 0, 1,59,55,0) #USER
print('Advance to next Spring....\n')
print('Set time 2am, March 30 UTC')
print('Timestamp now is ' + clk.set_GPS_time(spring) + '\n')
print('Finished test setting RTC from GPS.')

print('Now test DST rollover when time not updated externally\n')
"""#set RTC to 5 seconds before clocks go forward, UTC time minus zone"""
spring = (2024,3,31, 1, 59,55,0,0) #EU
#spring = (2024,3,10,9 ,59,55,0,0) #USA
#spring = (2024,4,25, 23,59,55,0,0) #EG
#spring = (2024,3,31, 1,59,55,0,0) #USER
clk.debug = False
print('Timestamp now is ' + clk.set_GPS_time(spring) + '\n')
print('Sleep for 6 seconds. DST_check = ',end=" ")
print(clk.dst_check)
sleep(5)
clk.debug = True
print('Timestamp now is ' + clk.get_timestamp_rtc() + '\n')



print('Advance to Autumn.')
print('Set time to 1:59:55 Oct 27 UTC')
autumn = (2024,10,27, 0, 59,55,0,0) #EU
#note: set hour early, as currently using summertime, GPS will add an hour.
clk.debug = False
print('Timestamp now is ' + clk.set_GPS_time(autumn) + '\n')
print('Sleep for 6 seconds. DST_check = ',end=" ")
print(clk.dst_check)
sleep(5)
clk.debug = True
print('Timestamp now is ' + clk.get_timestamp_rtc() + '\n')

print('Now test that TSYNC is returning the correct time NOW for configured timezone\n')

clk.set_debug(False)
isp = connect(station)
print(clk.set_NTP_time(isp))
