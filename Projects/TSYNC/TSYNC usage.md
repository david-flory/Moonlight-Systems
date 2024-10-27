TSYNC.py is a Micro Python class object providing functions to update and maintain the Real Time Clock for the ESP32 family of development boards.
TSYNC can update the RTC from either an NTP server or GPS module, and provide timestmps in a user configurable format for any location in the world.
When first initialised, or subsequently asked for a timestamp, TSYNC will check the current RTC time and update to daylight saving time accordingly as nescessary.

Initialisation.
Create an object instance of TSYNC with the following parameters. (zone, locale, separator, year_format, country, debug, hemisphere)
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
parts of British Columbia. Arizona does not use daylight saving time, but The Navaho Nation which is within Arizona does use daylight saving time.

Usage.
Import TSYNC
clock = TSYNC.TimeSync(0,1,0,0,'EU',True,False)
These params set the time zone to London, date format to [day month year], separator to [-], 4 digit year, country to 'EU' [Europe], Northern hemisphers, debug off.

Methods.
set_NTP_time(arg)
Takes 1 parameter which can be any positive integer.
Sets the RTC from an NTP server and returns the current timestamp on success, or "0" on failure.
Converts UTC time from server into current time for zone as configured.
Checks if hour needs to be added or not for daylight saving time.
The parameter is purely for convenience, and used to denote internet connection. Code exits if param is 0
For example your code could contain a function similar to below:

def get_internet_connection():
    do stuff to connect to wi-fi
	on connect return 1 else return 0

isp = 0
timestamp = TSYNC.set_NTP_time(isp)
Returns the current timestamp taking into account time zone and whether daylight saving time is in operation.

set_GPS_time(args)
Sets RTC using data from a GPS unit. 
Args are an 8 tuple of the format (year,month,mday,hour,minute,second,0,0)
Functions the same as set_NTP_time() in other respects.

get_timestamp_rtc()
Takes no parameters. 
Gets time from RTC, checks if hour needs to be added or subtracted for daylight saving time, and resets RTC if true.
Returns timestamp formatted as per configuration.

Utility programs.
Test_TSYNC north.py and Test_TSYNC south.py
Utilities for testing configuration of TSYNC

TSYNC_user setup.py
Utility for setting the time clocks go forward or back for the country USER.
This is for locations not covered by the generic EU, USA, EG, AUS, NZ, CHI settings.
For example, Jeruselem daylight saving starts earlier than the rest of Europe.

General information.

Set your code to call set_NTP_time() or set_GPS_time() straight after initialisation to ensure RTC is set correctly.
Thereafter, you can request timestamps from get_timestamp_rtc() without initiating another NTP or GPS update.
Be aware though that the ESP32 RTC gains around 30 to 40 seconds an hour, so possibly 16 minutes a day, so 
should be updated from NTP or GPS fairly regularly.

Caveats:
TSYNC does not enable the RTC to 'rollover' to summertime / wintertime automatically, however, it will do this if
either the time is set by NTP or GPS, or if a timestamp is requested from 'get_timestamp_rtc()'

The RTC will not be updated according to summertime / wintertime if deepsleep is used.
I do not see this as a bug, because by design, TSYNC sets the time correctly from the RTC on initialisation and records
a flag denoting if it is currently summer or winter. When a timestamp is requested, DST is adjusted according to whether it was 
summer or winter the previous time it was requested.

If your country does not use daylight saving time, this is not a problem.
If you set the time via NTP or GPS every time the ESP wakes, then also not a problem.
However, that is not always practical for low power projects, therefore a simple solution is to save and reset the flag
during each wake/sleep cycle using my RTC memory manager RMM.

See the demo utility tsync deepsleep test.py and the document deepsleep test.txt