from machine import deepsleep
import os
from time import sleep
import sys

def restore(file):
    try:
        os.rename(file + '.py', file + '.tmp')
        os.rename(file + '.bak', file + '.py')
        os.remove(file + '.tmp')
        print(file + '.py restored from backup, performing restart.\n\n')
        deepsleep(1000)
    except Exception as e:
        os.rename(file + '.tmp', file + '.py')
        print('No backup for ' + file)
        sys.exit(0)

sleep(2)
snooze = 0
#this will trap a compile errors from updates and restore a backup
#If your program is not called 'program.py' you must change this.
#It is case sensitive and do not write .py after the name
try:
    from program import maincode #change if name is different
except Exception as e:
        file = 'program' #change if name is different
        print('Error in ' + file + ': ' + str(e))
        restore(file)

print('Calling maincode\n\n')
try:
    snooze = maincode()
except Exception as e:
    file = 'program' #change if name is different
    print('Error in ' + file + ': ' + str(e))
    restore(file)

deepsleep(snooze)
