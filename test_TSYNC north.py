from time import sleep
import TSYNC
from machine import RTC

rtc = RTC()    
"""
UTILITY FOR TESTING TSYNC.py NORTHERN HEMISPHERE
zone, locale, separator, year_format, country
locale:
The desired date format: should be 1 to 3
1 = dd-mm-yyyy
2 = mm-dd-yyyy
3 = yyyy-mm-dd

separator: 0 for a hyphen, 1 for a slash.
year_format: 0 for 4 digit year, 1 for 2 digit year

Debug. True for verbose comments while running.
Hemisphere: True for North, False for South.
"""
year = 2024
#You may change this, but if you do you must also change
#the 3 spring and autumn dates below accordingly.

#set rtc outside of library to get set up correctly with a date before DST
reset_rtc = (year,1,20, 0, 1,59,55,0) #Any date in January
rtc.datetime(reset_rtc)
#initialise library
#Uncomment the country you want to test. The zone is set at 0 only for the purposes of this test.
clk = TSYNC.TimeSync(0,1,0,0,'EU',True,True) #EU
#clk = TSYNC.TimeSync(0,1,0,0,'USA',True,True) #USA and Canada
#clk = TSYNC.TimeSync(0,1,0,0,'EG',True,True) #Egypt
#clk = TSYNC.TimeSync(0,1,0,0,'USER',True,True) #User

clk.set_debug(True)
#pass a tuple of any date in this format: (year,month,mday,hour,minute,second,0,0)
print()
print('Timestamp now is ' + clk.get_timestamp_rtc())
print('DST is ',end=" ")
print(clk.dst_check)

#set rtc outside of library to 5 seconds to when clock should go forward
print()
print('Test putting clock forward')
spring = (2024,3,31, 0, 1,59,55,0) #EU
#spring = (2024,3,10, 0, 1,59,55,0) #USA
#spring = (2024,4,26, 0, 1,59,55,0) #EG
#spring = (2024,3,31, 0, 1,59,55,0) #USER

rtc.datetime(spring)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())
print()
print('Now test putting clock back again.')

#set rtc outside of library to 5 seconds to when clock should go back again
####this date should be UTC - 1 because RTC is on summertime now####
autumn = (2024,10,27, 0, 0,59,55,0) #EU
#autumn = (2024,11,3, 0, 0,59,55,0) #USA
#autumn = (2024,10,31, 0, 0,59,55,0) #EG
#autumn = (2024,10,27, 0, 0,59,55,0) #USER

rtc.datetime(autumn)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
print('DST is ',end=" ")
print(clk.dst_check)
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())

print()
print('Now set summertime next year')
#set rtc outside of library to 5 seconds to when clock should go forward next year
spring = (2025,3,30, 0, 1,59,55,0) #EU
#spring = (2025,3,9, 0, 1,59,55,0) #USA
#spring = (2025,4,25, 0, 1,59,55,0) #EG
#autumn = (2024,10,27, 0, 0,59,55,0) #USER

rtc.datetime(spring)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())
print()
print('Finished test.')
