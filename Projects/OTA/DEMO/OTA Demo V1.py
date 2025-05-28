import sys
import os
from time import sleep
import urequests as requests
import ubinascii
import network
#Any modules you import that are not built in to micropython
#must be error trapped like this. This will only raise compile
#errors so updated modules that crash can be restored from backup.
#Do not write .py after the module name.
try:
    import OTA
except Exception as e:
    raise Exception('OTA, ' + str(e))
#essential lines of your program
#The version number that will precede files on website that are downloadable.
ver = 'V2' #increment ver on each updated file
#actual version if you require it. It is not nescessary for OTA.py but I use it as confirmation updates are running sucsessfully
#by having the ESPs upload theis when they upload data, and I can see remotely which version is in use on all the ESPs in the group.
version = 'V1.0'
#URL pointing to the update location on the webserver.
upd_url  = "http://my_webserver/updates/test_ota.php?ver=" + ver #increment ver on each updated file
#Enter your WiFi network credentials here
ssid = 'xxxxxxxx'
pword = 'xxxxxxxx'
#the password you set for all the ESPs in your project. 
password = 'my_password'

#set a reference to the OTA class
ota = OTA.ota_updates()

station = network.WLAN(network.STA_IF)
station.active(False)

#your program should include a function to get an internet connection.
#Lets call it "get_connection"

def get_connection(station):
    station.active(True)
    count = 0
    station.connect(ssid,pword)
    while not station.isconnected():
        print('.', end="")
        sleep(1)
        count += 1
        if count > 30: break          
    if station.isconnected():
        print('WLAN connection to ' + ssid + ' succeeded!')
        return 1
    else:
        print('Unable to make connection after ' + str(count) + ' tries.')
        return 0

#This function calls OTA to check for updates
def check_update(url):
    isp = get_connection(station)
    result = ota.check_updates(url)
    if result == -1:
        print('No update files available')
        return(False)
    elif result == 0:
        print('Unable to contact server')
        return(False)
    else:
        print(str(result)  + ' files were updated')
        print('Deepsleep 1 second to install updates')
        return(True)
    
#The rest of your programs functions go here
#
#
#programs functions
#
#
#
#
#THIS IS THE ENTRY POINT OF YOUR PROGRAM
def maincode():
    #Creat a function maincode() and put these next few lines in it
    #followed by the rest of your program
    
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('\n\nMac address: ' + mac + '\n\n')
    mac = mac.replace(':','')  #strip out the colons from mac address
    url = upd_url + '&mac=' + mac + '&password=' + password + '&file='
    
    #From here, iinclude the rest of your program. If you are converting an existing program
    #pay attention to the scope of variables.
    #
    #rest of your program can overwrite this demo part
    #---------------------------------------------------------------------------------------
    print('\n\n')
    text = """This is the entry point of your program.
For the purposes of this demo, we shall call this 'OTA Demo', and it is version 1.
All it does is display this text and wait for your input.
Run 'Split_files.py' on 'OTA Demo V2' to prepare the chunks. Use the filenme 'program.py'
Upload the files to your webserver and then input 'y'."""
    print(text + '\n\n')
    print('Running OTA Demo.\nVersion is ' + version + '\n\n')
    
    x = input('Are you ready to update the program?  ')
    if x.upper() != 'Y': 
        raise Exception('program, Pressed any other key: Exit')
    #------------------------------------------------------------------------------------------
    #finally, at the point in your program where you want to check for updates
    #put these lines.
    print('Checking for updates....')
    upd = check_update(url)
    #returns True if update, False if not. 
    return(1000) #'Deepsleep to start new program
        
   
    