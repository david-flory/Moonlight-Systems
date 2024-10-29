from time import sleep
import sys
###Need to import RTC, deepsleep and RMM
from machine import RTC, deepsleep
import RMM
#set reference to RTC
rtc = RTC()
#check board and setup accordingly
board = sys.platform
print('\n')
print('Using ' + board)
if board == 'esp8266':
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rm = RMM.rtc_mem(491)
elif board == 'esp32':
    rm = RMM.rtc_mem(2047)
######Function required for RMM module########    
def save_vars():
    result = rm.save()
    for x in result:
        exec("z = " + x)
        rm.parse(z, x)
    writedata = rm.parse(z,'end')
    rtc.memory(writedata)
    
######PROGRAM START
#declare variables
hibernations = 0
rm.preserve(int,'hibernations')
counter = 0
rm.preserve(int,'counter')
prog_name = 'RTC memory manager quick demo.py'

#check for variables preserved before hibernation.
command = str(rtc.memory(),'UTF-8')
if command != '': exec(command)

#rest of program
if hibernations == 0:
    print('Hibernations = ' + str(hibernations) + '\nStarting counter\n')
elif hibernations == 1:
    print('Hibernations = ' + str(hibernations) + '\nContinue counter from where we left it.\n')
elif hibernations == 2:
    print('Hibernations = ' + str(hibernations) + '\nContinue counting then exit.\n')

for x in range(5):
    counter += 1
    print(counter)
    sleep(1)
print('Counter is ' + str(counter))
hibernations += 1

#Run this line to save preserved variables to rtc memory
#then go into hibernation
save_vars()

if hibernations < 3:
    print('\nHibernate for 3 seconds')
    if board == 'esp8266':
        rtc.alarm(rtc.ALARM0, 3000)
        deepsleep()
    deepsleep(3000)
else:
    print('End of demo\n\n')
    sys.exit(0)




