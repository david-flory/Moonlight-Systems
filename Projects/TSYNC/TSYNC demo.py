from time import sleep
import TSYNC
from utime import localtime, mktime, gmtime
from machine import RTC
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
def get_data(country, season, year):
    #country UK = 0, USA = 5, EG = 10, UK2025 = 15, USA2025 = 20, EG2025 = 25,  AUS = 30, NZ = 35, CHI = 40, AUS2025 = 45, NZ2025 = 50, CHI2025 = 55
    #date = 0,1,2,3,4 for Spring, Autumn, Spring, SpringDST and AutumnDST
    #need to get 0,1,2,3,4 for UK, 5,6,7,8,9 for USA etc
    #dates for 2024
    #EU 31/3 and 27/10
    data = [(2024, 3, 31, 2, 0,0,0,0),(2024, 10, 27, 2, 0,0,0,0),(2025, 3, 31, 2, 0,0,0,0),(2024, 3, 31, 1, 59,58,0,0),(2024, 10, 27, 0, 59,58,0,0)]#
    #USA 10/3 and 3/11 -8 hours
    data += [(2024, 3, 10, 10, 0,0,0,0),(2024, 11, 3, 10, 0,0,0,0),(2025,3,9, 10, 0,0,0,0),(2024, 3, 10, 9 ,59,58,0,0),(2024, 11, 3, 8,59,58,0,0)]#
    #EG 26/4 and 31/10 + 2 hours
    data += [ (2024, 4, 26, 0, 0,0,0,0),(2024,10,31, 0, 0,0,0,0),(2025,4,25, 0, 0,0,0,0,0),(2024,4,25, 23,59,58,0,0),(2024,10,30, 22,59,58,0,0)]#
    #AUS 6/10 and 7/4 + 10 hours
    data += [(2024,10,5, 16, 0,0,0,0),(2025,4,7, 16, 0,0,0,0),(2025,10,4, 16, 0,0,0,0),(2024,10,5, 15, 59,58,0,0),(2025,4,5, 14, 59,58,0,0)]#
    #NZ 29/9 and 7/4 + 12 hours
    data += [(2024,9,28, 14, 0,0,0,0),(2025,4,7, 14, 0,0,0,0),(2025,9,27, 14, 0, 0,0,0),(2024,9,28,13 ,59,58,0,0),(2025,4,5, 12,59,58,0,0)]#
    #CHI 8/9 and 7/4 - 4 hours
    data += [(2024, 9, 8, 6, 0,0,0,0),(2025, 4, 7, 6, 0,0,0,0),(2025, 9, 7, 6, 0,0,0,0),(2024, 9, 8, 5,59,58,0,0),(2025, 4, 6, 5,59,58,0,0) ]
    
    #dates for 2025
    #EU 30/3 and 26/10
    data += [(2025,3,30, 2, 0,0,0,0),(2025,10,26, 2, 0,0,0,0),(2026,3,29, 2, 0,0,0,0),(2025,3,30, 1, 59,58,0,0),(2025,10,26, 0, 59,58,0,0)]#
    #USA 9/3 and 2/11 - 8 hours
    data += [(2025,3,9, 10, 0,0,0,0),(2025,11,2, 10, 0,0,0,0),(2026,3,8, 10, 0,0,0,0),(2025,3,9,9 ,59,58,0,0),(2025,11,2, 8,59,58,0,0)]#
    #EG 25/4 and 30/10 + 2 hours
    data += [ (2025, 4, 25, 0, 0,0,0,0),(2025, 10, 30, 0, 0,0,0,0),(2026, 4, 24, 0, 0,0,0,0,0),(2025, 4, 24, 23,59,58,0,0),(2025, 10, 29, 23,59,58,0,0)]#
    #AUS 5/10 and 6/4 + 10 hours
    data += [(2025,10,4, 16, 0,0,0,0),(2026,4,6, 16, 0,0,0,0),(2026,10,3, 16, 0,0,0,0),(2025,10,4, 15, 59,58,0,0),(2026,4,4, 14, 59,58,0,0)]#
    #NZ 28/9 and 6/4 + 12 hours
    data += [(2025,9,27, 14, 0,0,0,0),(2026,4,5, 14, 0,0,0,0),(2026,9,26, 14, 0, 0,0,0),(2025,9,27,13 ,59,58,0,0),(2026,4,4, 12,59,58,0,0)]#
    #CHI 7/9 and 6/4 - 4 hours
    data += [(2025, 9, 7, 6, 0,0,0,0),(2026, 4, 6, 6, 0,0,0,0),(2026, 9, 6, 6, 0,0,0,0),(2025, 9, 7, 5,59,58,0,0),(2026, 4, 5, 4,59,58,0,0) ]
    
    C = 0
    if country == 'USA':  C = 1
    elif country == 'EG': C = 2
    elif country == 'AUS': C = 3
    elif country == 'NZ': C = 4
    elif country == 'CHI': C = 5
    C *= 5
    index = (season + C)
    if year == 2025: index += 30
    if index > 59: index = 0
    return data[index]

def dst():
    if clk.dst_check == False: return '  Currently using Winter time'
    else: return '  Currently using Summer time'

#Change ssid and password to your credentials to obtain internet connection
ssid = 'xxxxxxxxx'
password = 'xxxxxxxxx'

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
#year = 2025
country = input ('Enter the country you want to test from EU, USA, EG, AUS, NZ, CHI : ').upper()
country_list = ['EU','USA','EG','AUS','NZ','CHI']
if (country_list.count(country)) == 0:
    print('country is invalid')
    sys.exit(0)


#initialise library
if country == 'EU':
    clk = TSYNC.TimeSync(0,1,0,0,'EU',True)
elif country == 'USA':
    clk = TSYNC.TimeSync(-8,1,0,0,'USA',True)
elif country == 'EG':
    clk = TSYNC.TimeSync(2,1,0,0,'EG',True)
elif country == 'AUS':
    clk = TSYNC.TimeSync(10,1,0,0,'AUS',False)
elif country == 'NZ':
    clk = TSYNC.TimeSync(12,1,0,0,'NZ',False)
elif country == 'CHI':
    clk = TSYNC.TimeSync(-4,1,0,0,'CHI',False)


#set rtc with UTC time using  GPS
#(year,month,mday,hour,minute,second,0,0)
gps_tuple = (year,1,1,10,0,0,0,0) #Any date in January 
#turn on verbose messages
clk.debug = True
#set rtc with UTC time using  GPS
#(year,month,mday,hour,minute,second,0,0)
gps_tuple = (year,1,1,10,0,0,0,0) #Any date in January
print('Time now is ' + clk.set_GPS_time(gps_tuple) + '\n')
clk.debug = False
print ('Advance to 2am Spring time. TSYNC will advance clock to 3am')
print('Timestamp now is ' + clk.set_GPS_time(get_data(country,0,year)) + dst() )
print('Advance to 2am next Autumn.')
print('Timestamp now is ' + clk.set_GPS_time(get_data(country,1,year)) + dst())
print ('Advance to 2am next Spring. TSYNC will advance clock to 3am')
print('Timestamp now is ' + clk.set_GPS_time(get_data(country,2,year)) + dst())
print('\nFinished test setting RTC from GPS.')

print('Now test DST rollover when time not updated externally\n')
clk.dst_check = False
print('Timestamp now is just before clocks go forward ' + clk.set_GPS_time(get_data(country,3,year)) + dst())
print('sleep for 3 seconds')
sleep(3)
clk.debug = True
print('Timestamp now is ' + clk.get_timestamp_rtc() + '\n')
clk.debug = False
print('Timestamp now just before clocks go back ' + clk.set_GPS_time(get_data(country,4,year)))
print('sleep for 3 seconds')
sleep(3)
clk.debug = True
print('Timestamp now is ' + clk.get_timestamp_rtc())
clk.debug = False

print('Now test that TSYNC is returning the correct time NOW for configured timezone\n')

clk.set_debug(False)
isp = connect(station)
if isp == 0:
    print('No internet connection')
    sys.exit(0)
print(clk.set_NTP_time(isp)+'\n')














