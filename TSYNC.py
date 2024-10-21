from ntptime import settime
from utime import localtime, mktime, gmtime
from machine import RTC
rtc = RTC()
"""
Copyright (c) 2024 David Flory  www.moonlight-systems.co.uk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use
in the Software without restriction, including without limitation the rights
to copy, modify, merge, publish, distribute, copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE

Parameters
zone:
The offset from UTC of your time zone. Must be between -12 to +12
Any parameter outside this range will return UTC time
Decimal fractions are accepted, ie India at 4.5

locale:
The desired date format: should be 1 to 3
1 = dd-mm-yyyy
2 = mm-dd-yyyy
3 = yyyy-mm-dd

separator: 0 for a hyphen, 1 for a slash.
year_format: 0 for 4 digit year, 1 for 2 digit year

Country:
Used for daylight saving time. The list is generalised, and not region specific.
EU covers Europe, including Greenland.
AUS covers Australia
NZ for New Zealand
CHI for Chile
USA for USA, Mexico, Canada, Turks & Caicos and Carribean
EG for Egypt
NA for no daylight saving.
USER for manual settings. Use the supplied utility "manual_setup.py" to obtain offsets.
Note: For total accuracy, double check the above settings are correct for your location.
For example, USA is correct for most of USA and Canada, but certain areas are different, such as Yukon, most of Saskatchewan and
parts of British Columbia. Arizona is also not the same as the rest of USA.
#useful resource for checking or testing your settings https://www.timeanddate.com/time/map/

Debug: If True gives verbose comments during operation. Main use is for testing setup.
Hemisphere: True for northern hemisphere, false for southern hemisphere
typical usage for UK timestamp is (0,1,0,1,'EU',True,False)
"""
class TimeSync:
    def __init__(self, zone, locale, separator, year_format, country, hemisphere, debug):
        if isinstance(zone, float):
            self.zone = int(zone)
            self.zone_add = int((zone - self.zone) * 3600)
        else:
            self.zone = zone
            self.zone_add = 0
        self.locale = locale
        self.separator = separator
        self.year_format = year_format
        self.country = country
        self.dst_1 = 0
        self.dst_2 = 0
        self.dst_check = False
        self.debug = debug
        self.hemisphere = hemisphere
        self.year = 0
        self.month = 0
        self.mday = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.weekday = 0
        self.yearday = 0
        self.get_DST()
  
    def set_debug(self, arg):
        self.debug = arg

    def set_localtime(self,args):
        if args == 1:
            rtc_tuple = (self.year, self.month, self.mday, self.weekday, self.hour, self.minute, self.second, 0)
            return rtc_tuple
        if args == 0:
            (self.year, self.month, self.mday, self.hour, self.minute, self.second, self.weekday, self.yearday) = localtime()
        if args > 1000:
            (self.year, self.month, self.mday, self.hour, self.minute, self.second, self.weekday, self.yearday) = localtime(args)
      
    def get_DST(self,):
        #sets yearday of when clocks go forward and back by counting back from 7 days after that date of the month.
        #The offset is the number of days from the EU or AUS yearday to the yearday for the specific country.
        #if country does not use DST self.dst_1 remains set to 0 and self.dst_check is false.
        self.set_localtime(0)
        epoch_now = mktime(localtime())
        if self.hemisphere:
            d = 31
            m = 3
            if self.country == 'NA':
                return
            if self.country == 'EU':
                if self.debug: print('Country is EU')
                offset = 0 #last sunday of March
            if self.country == 'USA':
                if self.debug: print('Country is USA')
                offset_days = -21 # second sunday in March
                offset = 86400 * offset_days
            elif self.country == 'EG':
                if self.debug: print('Country is EG')
                offset_days = 26 # #Last Friday in April 
                offset = 86400 * offset_days
            elif self.country == 'USER': 
                if self.debug: print('Country is USER')
                offset_days = 0 #Set this offset manually
                offset = 86400 * offset_days
            #calculate DST epochs for EU country, where offset == 0
            args1 = (self.year,m,1,23,0,0,0,0)
            args2 = (self.year,m,d,23,0,0,0,0)
        else:
            m = 10
            d = 7
            if self.country == 'AUS':
                if self.debug: print('Country is AUS')
                offset_days = 0 #First Sunday Oct
                offset = 86400 * offset_days
            elif self.country == 'NZ':
                if self.debug: print('Country is NZ')
                offset_days = -7 #Last Sunday September
                offset = 86400 * offset_days
            elif self.country == 'CHI':
                if self.debug: print('Country is CHI')
                offset_days = -28 # First Sunday September
                offset = 86400 * offset_days
            elif self.country == 'USER': 
                if self.debug: print('Country is USER')
                offset_days = 0 #Set this offset manually
                offset = 86400 * offset_days
            #calculate DST epochs for AUS country, where offset == 0
            args1 = (self.year,m,1,23,0,0,0,0) 
            args2 = (self.year,m,d,23,0,0,0,0) 
        #calculate DST epochs for EU country, where offset == 0
        epoch = mktime(args1) #epoch of 1st day of month, 23:00
        ts = localtime(epoch)
        s_day = ts[7] #yearday of 1st of month
        epoch = mktime(args2) #epoch of last day of month, 23:00
        ts = localtime(epoch)
        yearday = ts[7] #yearday of end of month
        day = ts[6] #day of the week
        if day == 6: #a sunday
            spring_day = yearday
        for x in range(5, -1, -1):
            if day == x:
                spring_day = yearday - x -1
        #spring_day is the day in spring [April] clocks go forward in current year for country = EU.
        #As it is extremely unlikely this will not be run again between Jan to March being set after
        #this date is not considered a problem, as it will be reset after december.
        #get epoch of 1 second before 2am of that day.
        args = (self.year, m, spring_day - (s_day - 1), 1, 59, 59, 0, 0)
        #args are correct for EU and AUS, use offset to adjust
        epoch = mktime(args) + offset

        self.dst_1 = epoch
        if self.country == 'NA': 
            return
        if self.hemisphere:
            d = 31
            m = 10
            if self.country == 'EU': #last sunday October
                offset = 0
            elif self.country == 'USA': #first sunday November
                offset_days = 7
                offset = 86400 * offset_days
            elif self.country == 'EG': #last thursday October
                offset_days = 4
                offset = 86400 * offset_days
            elif self.country == 'USER': 
                offset_days = 0 #Set this offset manually
                offset = 86400 * offset_days
            args1 = (self.year,m,1,23,0,0,0,0)
            args2 = (self.year,m,d,23,0,0,0,0)
        else:
            d = 7
            m = 4
            if self.country == 'AUS': #First Sunday April
                offset_days = 0
                offset = 86400 * offset_days
            elif self.country == 'NZ': #First Sunday April
                offset_days = 0
                offset = 86400 * offset_days
            elif self.country == 'CHI': #First Saturday April
                offset_days = 0 
                offset = 86400 * offset_days
            elif self.country == 'USER': 
                offset_days = 0 #Set this offset manually
                offset = 86400 * offset_days
            args1 = (self.year,m,1,23,0,0,0,0) 
            args2 = (self.year,m,d,23,0,0,0,0) 
        epoch = mktime(args1) 
        ts = localtime(epoch)
        s_day = ts[7] 
        epoch = mktime(args2)
        ts = localtime(epoch)
        yearday = ts[7] 
        day = ts[6] #day of the week
        if day == 6: #sunday
            fall_day = yearday 
        for x in range(5, -1, -1):
            if day == x:
                fall_day = yearday - x -1 
        #fall_day is the day in Autumn [October] clocks go back in current year for country EU.
        #As it is extremely unlikely this will not be run again between Oct to Jan being set after
        #this date is not considered a problem, as it will be reset after december.
        #get epoch of 1 second before 2am of that day.
        args = (self.year, m, fall_day - (s_day - 1), 1, 59, 59, 0, 0)
        epoch = mktime(args) + offset
        self.dst_2 = epoch
        epoch = mktime(localtime())
        if self.debug: print('Current date from RTC ',end=" ")
        if self.debug: print(self.get_timestamp(epoch))

        if self.hemisphere:
            if epoch > self.dst_1 and epoch < self.dst_2: self.dst_check = True
        else:
            self.dst_check = True
            if epoch > self.dst_2 and epoch < self.dst_1: self.dst_check = False

        if self.debug:
            if self.dst_check:
                print('Using summer time')
            else:
                print('Using winter time [UTC]')
            print('Summertime starts on ' + self.get_timestamp(self.dst_1))
            print('Clocks go back on ' + self.get_timestamp(self.dst_2))
            
    def get_timestamp_rtc(self): 
        adjust = 0
        self.set_localtime(0)
        days= {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
        months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        #make adjustment for daylight saving time
        epoch = mktime(localtime())
        if self.hemisphere:
            if not self.dst_check and epoch > self.dst_1:
                if self.debug: print('Clocks need to go forward.')
                epoch += 3600
                self.set_localtime(epoch)
                rtc.datetime(self.set_localtime(1))
                self.dst_check = True
                if self.debug: print('Daylight saving is on')
            if self.dst_check and epoch > self.dst_2:
                if self.debug: print('Clocks need to go back.')
                epoch -= 3600
                self.set_localtime(epoch)
                rtc.datetime(self.set_localtime(1))
                self.dst_check = False
                if self.debug: print('Daylight saving is off')
        else:

            if self.dst_check and epoch > self.dst_2:
                if self.debug: print('Clocks need to go back.')
                epoch -= 3600
                self.set_localtime(epoch)
                rtc.datetime(self.set_localtime(1))
                self.dst_check = True
                if self.debug: print('Daylight saving is on')
            if not self.dst_check and epoch > self.dst_1:
                if self.debug: print('Clocks need to go forward.')
                epoch += 3600
                self.set_localtime(epoch)
                rtc.datetime(self.set_localtime(1))
                self.dst_check = False
                if self.debug: print('Daylight saving is off')
        
        ts = localtime()
        #add leading zero to hour
        if ts[3] > 9:
            t = str(ts[3]) + ':'
        else:
            t = '0' + str(ts[3]) + ':'
        #add leading zero to minute
        if ts[4] > 9:
            t += str(ts[4]) + ':'
        else:
            t += ('0' + str(ts[4])) + ':'
        #add leading zero to seconds
        if ts[5] > 9:
            t += str(ts[5])
        else:
            t += ('0' + str(ts[5]))
        #add leading zero to day
        if ts[2] > 9:
            dy = str(ts[2])
        else:
            dy = ('0' + str(ts[2]))
        #add leading zero to month
        if ts[1] > 9:
            mt = str(ts[1])
        else:
            mt = ('0' + str(ts[1]))
        #format the timestamp
        str_year = str(ts[0])
        if self.year_format == 1:
            str_year = str_year[2:]
        if self.separator == 1:
            sep = '/'
        else:
            sep = '-'
        if self.locale == 1:
            d = dy + sep + mt + sep + str_year
        elif self.locale == 2:
            d = mt + sep + dy + sep + str_year
        elif self.locale == 3:
            d = str_year + sep + mt + sep + dy
        timestamp = d + ' ' + t
        return(timestamp) #as a string

    def set_NTP_time(self,isp):
        if isp == 0: return False
        count = 0
        if self.debug: print('Setting RTC from NTP server')
        while count < 5:
            try:
                settime()
                #RTC now current UTC time
                self.update_dst()
                return True
            except Exception as e:
                print(str(e))
                count += 1
                #if str(e) == '[Errno 116] ETIMEDOUT':
        return False
    
    def update_dst(self):
        epoch = mktime(localtime())
        epoch += (self.zone * 3600) #ammend for time zones
        if self.zone_add > 0: epoch += self.zone_add
        #rtc is now set according to time zone as UTC
        if self.country != 'NA': #DST used for this country
            #RTC will be UTC time at this point.
            self.get_DST()
            # set DST parameters again, as RTC previously could have been 1/1/2000 after a power on reset
            #If RTC time + hour > start of summertime set Summertime on
            if self.dst_check: epoch += 3600
        self.set_localtime(epoch)
        rtc.datetime(self.set_localtime(1))
        #rtc is now set according to time zone and DST
        
    def set_GPS_time(self, args):
        #most GPS return a UTC time. You will need to check the format
        #it takes from your particular GPS unit. This function uses the format returned
        #by the Adafruit Ultimate GPS breakout which is an 8 tuple of the format
        #(year,month,mday,hour,minute,second,0,0)

        if self.debug: print('Setting RTC from GPS fix')
        epoch = mktime(localtime())
        epoch += (self.zone * 3600) #ammend for time zones
        if self.zone_add > 0: epoch += self.zone_add
        self.set_localtime(epoch)
        #(year, month, mday, hour, minute, second, weekday, yearday) = localtime(epoch)
        #rtc_tuple = (year, month, mday, weekday, hour, minute, second, 0)
        rtc.datetime(self.set_localtime(1))
        #RTC is now set to UTC time for location
        update_dst(self)
        #RTC now reset allowing for DST
    
#The following functions not used by any of the above, but left here as utilities
#that may be useful. Some are used by the testing utilities.
    
    def get_timestamp(self,epoch): 
        #returns timestamp as a string from passed epoch or if 0, gets epoch from timestamp
        #UK formatted timestamp, ie dd-mm-yyyy hr:min:secs
        if epoch == 0:
            ts = localtime()
        else:
            ts = localtime(epoch)
        if ts[3] > 9:
            t = str(ts[3]) + ':'
        else:
            t = '0' + str(ts[3]) + ':'
        if ts[4] > 9:
            t += str(ts[4]) + ':'
        else:
            t += ('0' + str(ts[4])) + ':'  
        if ts[5] > 9:
            t += str(ts[5])
        else:
            t += ('0' + str(ts[5])) 
        if ts[2] > 9:
            dy = str(ts[2])
        else:
            dy = ('0' + str(ts[2]))
        if ts[1] > 9:
            mt = str(ts[1])
        else:
            mt = ('0' + str(ts[1]))
        d = dy + '-' + mt + '-' + str(ts[0])
        uk_time = d + ' ' + t
        return(uk_time) #as a string

    def  get_weekday(self,year,month,mday):
        #get weekday from date passed as a tuple
        #(year, month, mday, hour, minute, second, weekday, yearday) = localtime()
        args = (year,month,mday,0,0,0,0,0)
        epoch = mktime(args)
        days= {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
        timestamp = localtime(epoch)
        return days[timestamp[6]]

    def debug_test(self, data):
        #use for checking your timezone and daylight saving are correct.
        #pass a tuple of any date in this format: (year,month,mday,hour,minute,second,0,0)
        if self.debug: print('Debug is on.')
        epoch = mktime(data)
        print('Epoch now is ',end=" ")
        print(epoch)
        #set the rtc
        self.set_localtime(epoch)
        rtc.datetime(self.set_localtime(1))
        print('After manual RTC reset rtc tuple is ',end=" ")
        print(self.set_localtime(1))
        timestamp = self.get_timestamp_rtc()
        return timestamp
