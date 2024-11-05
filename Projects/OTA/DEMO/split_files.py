"""Copyright (c) 2024 David Flory  www.moonlight-systems.co.uk
Requirements: Python3"""

import sys
import os
#limits files to less than 4Kb, actually around 3500 characters.
mac = ''
download_data = []

def split_program():
    global download_data
    global mac
    x = 0
    chunks = 0
    flag = 0
    mac = ''
    tempdata=[]
    mac = input('Enter mac address for unit to update [preceded by V no.] : ')
    process = 0
    while process == 0:
        file = input('Enter filename of file to process or Enter to finish : ')
        if file == '' or file.upper() == 'N':
            process = 1
            print()
        else:
            prog = input('Enter filename as run on the ESP : ')
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
            upd = mac.replace(':','') + str(x)
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
upd = mac.replace(':','') + '_data'
f = open(upd,'w')
f.write(tempdata)
f.close()
