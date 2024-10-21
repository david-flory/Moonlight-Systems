from time import sleep
import TSYNC
from utime import localtime, mktime, gmtime
from machine import RTC

rtc = RTC()    

"""
UTILITY FOR TESTING TSYNC.py SOUTHERN HEMISPHERE
TSYNC parameters: zone, locale, separator, year_format, country, debug, hemisphere
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

#set rtc outside of library 
reset_rtc = (year,1,20, 0, 1,59,55,0) #Any date in January 
rtc.datetime(reset_rtc)
#initialise library
#Uncomment the country you want to test. The zone is set at 0 only for the purposes of this test.

#clk = TSYNC.TimeSync(0,1,0,0,'AUS',False,True) #Australia
#clk = TSYNC.TimeSync(0,1,0,0,'NZ',False,True) #New Zealand
clk = TSYNC.TimeSync(0,1,0,0,'CHI',False,True) #Chile
#clk = TSYNC.TimeSync(0,1,0,0,'USER',True,True) #User settings
#sys.exit(0)
clk.set_debug(True)
#pass a tuple of any date in this format: (year,month,mday,hour,minute,second,0,0)
print()
print('Timestamp now is ' + clk.get_timestamp_rtc())
print('DST is ',end=" ")
print(clk.dst_check)

print()
print('Test setting clock to wintertime')
#set rtc outside of library to 5 seconds before clock should go back
####this date should be UTC - 1 because RTC is on summertime now####
#autumn = (2024,4,7, 0, 0,59,55,0) #AUS
#autumn = (2024,4,7, 0, 0,59,55,0) #NZ
autumn = (2024,4,7, 0, 0,59,55,0) #CHI
#autumn = (2024,4,7, 0, 0,59,55,0) #USER

rtc.datetime(autumn)
clk.set_debug(False)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
clk.set_debug(True)
print('DST is ',end=" ")
print(clk.dst_check)
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())
print('Now check setting clock to summertime')

#set rtc outside of library to 5 seconds before clock should go forward
print()
print('Test putting clock forward')
#spring = (2024,10,6, 0, 1,59,55,0) #AUS
#spring = (2024,9,29, 0, 1,59,55,0) #NZ
spring = (2024,9,8, 0, 1,59,55,0) #CHI
#spring = (2024,9,29, 0, 1,59,55,0) #USER
rtc.datetime(spring)
clk.set_debug(False)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
clk.set_debug(True)
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())
print()
print('Now test putting clock back again.')

print()
#print('Now set summertime next year')
#set rtc outside of library to 5 seconds before clock should go forward next year
#spring = (2025,4,6, 0, 0,59,55,0) #AUS (UTC +1)
#spring = (2025,4,6, 0, 1,59,55,0) #NZ
spring = (2025,4,6, 0, 1,59,55,0) #CHI
#spring = (2025,4,6, 0, 1,59,55,0) #USER

rtc.datetime(spring)
clk.set_debug(False)
clk.update_dst()
print('Timestamp is ' + clk.get_timestamp_rtc())
clk.set_debug(True)
print('Sleep for 5 seconds.')
sleep(5)
print('Timestamp is ' + clk.get_timestamp_rtc())
print()
print('Finished test.')
