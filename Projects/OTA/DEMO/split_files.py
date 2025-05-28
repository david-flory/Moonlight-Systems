"""Copyright (c) 2024 David Flory  www.moonlight-systems.co.uk
Requirements: Python3

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
THE SOFTWARE"""

import sys
import os
#limits files to less than 4Kb, actually around 3500 characters.
mac = ''
download_data = []
ver = ''

def split_program():
    global download_data
    global mac
    global ver
    x = 0
    chunks = 0
    flag = 0
    mac = ''
    tempdata=[]
    program = 'program.py'
    ver = 'V' + input('Enter version number of program to be updated, [without the V] : ')
    mac = input('Enter mac address for unit to update : ')
    file = input('Enter filename of file to process: ')
    prog = input('Enter filename as run on the ESP or just Enter for program.py: ' )
    if prog == '': prog = program
    tempdata.append(file)
    tempdata.append(prog)
    maxline = 0
    lines = 0
    count = 0
    for c in tempdata:
        count += 1    
    for c in range(0,count, 2):
        file = tempdata[c]
        prog = tempdata[c + 1]  
        try:
            f = open(file,"r")
            z = f.readlines()
            maxline = len(z)
            f.close()
            f = open(file,"r")
        except Exception as e:
            print('open failed with ' + str(e))
            sys.exit(0)
        chars = 0
        flag = 0
        lines = 0
        while flag != 1:
            upd = ver + mac.replace(':','') + str(x)
            f2 = open(upd,'w')
            while chars < 3500:
                line = f.readline()
                chars += len(line)
                f2.write(line)
                lines += 1
                if lines >= maxline:
                    flag = 1
                    #print('flag == 1')
                    break
            f2.close()
            x += 1
            chunks += 1
            chars = 0
        f.close()
        download_data.append(prog)
        download_data.append(chunks)
        chunks = 0

split_program()

tempdata = ''
for x in download_data:
    tempdata += str(x) + ','

print('Files created for upload:   Filename on ESP,  Number of chunks.\n')
print(tempdata)
upd = ver + mac.replace(':','') + '_data'
f = open(upd,'w')
f.write(tempdata)
f.close()
