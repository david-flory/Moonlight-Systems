RMM.py is a micropython class module for the ESP32 to facillitate easy saving of variables to RTC memory, and restoring them when a program wakes from deepsleep.
Tested on Adafruit ESP32 feather v2  and ESP8266 NodeMCU which has only 492 bytes. 
The ESP32 is supposed to hav 4K of useable RTC memory, but in my tests my board would only accept 2048 bytes.
My ESP8266 NodeMCU tested out as expected, with 492 bytes.
The data types accepted are string, set, list, tuple, int, float and bool. Multiline strings are accepted but linefeed characters are stripped out when saved to the rtc memory.

More useful for the 8266, if the data to be saved exceeds 491 bytes, the data is written to flash memory instead. It is still restored seamlessly after deepsleep.

See RMM details.txt and demo file for for detailed info on using RMM.py.
