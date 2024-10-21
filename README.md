TSYNC is a micropython class library for the ESP32 that implements maintaining the RTC
and handling changing time to UTC or daylight saving time for any country or time zone.
Its functions include:
1) Setting the RTC from either an NTP server or GPS module
2) Returning a timestamp formatted to several user configured formats, for user configured country.
When either of the above two functions a called, the RTC is updated for daylight saving time.

The included utilities test_TSYNC south.py and test_TSYNC north.py are to test operation of the class
and TSYNC_user setup.py for configuring the start and end of daylight saving time for a country not included 
in the preset configuration. For example, Arizona does not observe DST except for the Navaho nation which does.
