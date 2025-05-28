"""Copyright (c) 2024 David Flory  www.moonlight-systems.co.uk

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

import urequests as requests
import os

class ota_updates:
    def __init__(self):
        self.download_data = []
        self.updated = []

    def parse(self, string):
        count = string.count(',')
        for x in range(0,count,2):
            y = string.find(',')
            self.download_data.append(string[0:y])
            string = string[y+1:]
            y = string.find(',')
            self.download_data.append(string[0:y])
            string = string[y+1:]
        
    def check_updates(self, url):
        try:
            print(url + '_data')
            response = requests.get(url + '_data')
        except:
            print('request failed')
            return 0 #unable to get response from server
        x = response.text.find('File not found')
        if x == -1:
            command = response.text.strip()
            self.parse(command)
            result = self.update_program(url)
            self.download_data.clear()
            return result
        else:
            response.close
            return -1 #no files to download
        response.close()
        
    def update_program(self, url):
        programs_updated = 0
        #count how many programs to download
        c = 0
        for x in self.download_data:
            c += 1
        total_files = 0
        for a in range(0, c, 2):
            total_files += int(self.download_data[a+1])
            #print('There are ' + str(total_files) + ' for ' + self.download_data[a])
            program_name = self.download_data[a]
            file_count = int(self.download_data[a +1])
            #print('Program name = ' + program_name)
            #print('No of files = ' + str(file_count))
            dot = program_name.find('.')
            tmp_name = program_name[:dot]
            f = open(tmp_name + '.tmp','w')

            for x in range(file_count):
                update = 1
                #download it
                #print('Downloading ' + program_name + ' file no ' + str(x))
                for y in range(3):
                    try:
                        URL = url + str(x)
                        print(URL)
                        response = requests.get(URL)
                        break
                    except:
                        print('request failed')
                if y == 2:
                    print('Tried 3 times for file ' + mac + str(x))
                    f.close()
                    update = 0
                    self.download_data.clear()
                    return 0 #indicates files available but server error
                fail = response.text.find('File not found')
                #write the file
                if fail == -1:
                    try:
                        data = response.text
                        data = data.lstrip('\n')
                        f.write(data)
                        data = ''
                        f.flush()
                        response.close()
                        #print('Writing '+ program_name + ' file no ' + str(x))
                    except Exception as e:
                        print('Error writing file:  ' + str(e))
                        f.close()
                        update = 0
                        response.close()
                        data = ''
                        gc.collect()
                        return 0 #indicates files available but os error
                #back up to get next file
            if update == 1:
                #All downloaded, close the file and update filesystem
                f.close()
                #check if this file is present in the filesystem
                try:
                    #print('Updating filesystem')
                    dot = program_name.find('.')
                    tmp = program_name[:dot]
                    os.rename(tmp + '.bak', tmp)
                    #if no exception, there was a backup, so there is a python file too
                    os.rename(tmp + '.py', tmp + '.bak') #create backup
                    os.remove(tmp) #remove the file we just created (tmp)
                    os.rename(tmp + '.tmp', tmp + '.py')#overwrite old file with downloaded file
                    #print('old ' + program_name + ' backed up and new file written')
                    programs_updated += 1
                    self.updated.append(program_name)
                except:
                    #backup does not exist, try python file
                    try:
                        os.rename(tmp + '.py', tmp + '.bak')
                        #if no exception, there was a python file and we just created a backup
                        os.rename(tmp + '.tmp', tmp + '.py')
                        #print(program_name + ' backed up and new file written')
                        programs_updated += 1
                        self.updated.append(program_name)
                    except:
                        #python file does not exist, so it is a new file, maybe a library
                        os.rename(tmp + '.tmp', tmp + '.py')
                        #print('New file ' + program_name + ' written.')
                        programs_updated += 1
                        self.updated.append(program_name)
            update = 0     #start again if more programs to download       
        return programs_updated        
