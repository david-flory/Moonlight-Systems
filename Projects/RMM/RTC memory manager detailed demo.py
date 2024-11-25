from time import sleep
import sys
###Need to import RTC, deepsleep and RMM
from machine import RTC, deepsleep
import RMM
#set reference to RTC
rtc = RTC()
#check board and setup accordingly
board = sys.platform
print('\n\n\n')
print('Using ' + board)
sleep(2) #included to give time to break code before cycling into deepsleep
if board == 'esp8266':
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rm = RMM.rtc_mem(491)
elif board == 'esp32':
    rm = RMM.rtc_mem(2047)

rm.debug = True  #prints info messages for testing or debugging
######Function required for RMM module########    
def save_vars():
    result = rm.save()
    for x in result:
        exec("z = " + x,  None, globals())
        rm.parse(z, x)
    writedata = rm.parse(z,'end')
    rtc.memory(writedata)
    
######PROGRAM START
"""normal program procedure:
Explicitly declare variables we want to survive after hibernation
each one has to be declared as a type, ie my_string = '' or my_int = 0
though the value is unimportant.
Each variable also has to be declared to the RMM class, with name and 
data type, ie "rm.preserve(str, 'my_string')"
"""
chunk = """xxxxxxx"""
rm.preserve(str, 'chunk')
my_string = ''
rm.preserve(str, 'my_string')
my_float = 0.1
rm.preserve(float, 'my_float')
my_list = []
rm.preserve(list, 'my_list')
my_tuple = ()
rm.preserve(tuple, 'args')
my_set = {}
rm.preserve(set, 'my_set')
my_bool = False
rm.preserve(bool, 'my_bool')
my_int = 0
rm.preserve(int, 'my_int')
hibernations = 0
rm.preserve(int,'hibernations')
"""The following variables will not survive hibernation because
we have not declared them to the RMM class"""
counter =0
delay = 0
timer = 0.5
prog_name = 'RTC memory manager demo.py'

#Every time program starts, whether from power on reset or
#wake from hibernation, variables are declared

#Then check for stored variables from previous operations and
#if found, overwrite the previously declared values.
command = str(rtc.memory(),'UTF-8')
if command == '':
    """if blank, rtc.memory is unset, so this is the first time
    program has run, typically a power on reset. Program runs normally
    doing tasks etc. Usually as it runs a program would assign and re-assign
    values to variables as it runs, but for the purposes of this demo we will do
    it here, as there is no "programme" as such."
    NOTE we do not need to update the RMM class, as that was done in declaration."""
    
    print('RTC empty, assign variable values for first time.')
    if board == 'esp8266':
        chunk = """This is a huge chunk of data intended to fill up the rtc memory to test its limits.
        This chunk to test Esp8266. Including the saved variables, 490 bytes will be saved in the rtc memory.
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
        #add "plus some extra to force file save" to above to test saving / restoring from file

    else:
        chunk = """
        To test Esp32, this chunk is bigger.
        Including the saved variables, 2047 bytes will be saved to rtc memory.
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
        #add "plus some extra to force file save" to above to test saving / restoring from file
    my_string = 'This is a very important string'
    my_float = 1056.98
    my_list = list(("apple", 1.25, True))
    args = (0,1,12,46,'UK',True)
    my_set = set(("apple", "banana", "cherry",False,1.25,1))
    my_bool = False
    my_int = 250
    counter = 25
    delay = 8
    timer = 12.5
    prog_name = ''
else:
    print('Found data in rtc memory.')
    exec(command,  None, globals())
    print('Previous variables restored.\n')
    print(chunk)
    print('my_string = ',end=" ")
    print(my_string)
    print('my_list = ',end=" ")
    print(my_list)
    print('my_set = ',end=" ")
    print(my_set)
    print('my_tuple = ',end=" ")
    print(my_tuple)
    print('my_int = ',end=" ")
    print(my_int)
    print('my_float = ',end=" ")
    print(my_float)
    print('my_bool = ',end=" ")
    print(my_bool)
    print('hibernations = ' + str(hibernations))
    print('Unsaved variables not restored')
    print('counter = ' + str(counter))
    print('delay = ' + str(delay))
    print('timer = ' + str(timer))
    print('prog_name = ',end=" ")
    print(prog_name)

#Eventually we reach a point in the program when we want to hibernate.
print('Program runs for 5 seconds.')
a = 0
while a < 5:
    sleep(1)
    print('.',end="")
    a +=1

hibernations += 1

#Run this line to save preserved variables to rtc memory
#then go into hibernation
save_vars()

if hibernations < 2:
    print('\nHibernate for 3 seconds')
    if board == 'esp8266':
        rtc.alarm(rtc.ALARM0, 3000)
        deepsleep()
    deepsleep(3000)
else:
    print('End of demo\n\n')
    sys.exit(0)
