import os
from machine import Pin, SoftSPI
try:
    import sdcard
except:
    pass
    
class fm_init_sd:
    def __init__(self, spi_pins = (0,0,0,0,0,0)):
        self.pwr = 0
        if spi_pins[5] > 0:
            self.pwr = spi_pins[5]
            self.sd_pwr = Pin(self.pwr, Pin.OUT, Pin.PULL_DOWN)
        self.spi_pins = spi_pins
        self.SD = False
        if spi_pins[0] > 0: self.SD = self.Start_SD(spi_pins)
           
    def is_sd(self):
        return self.SD
        
    def is_exist(self):
        #check if the file exists, if not, create an empty file
        #else open and read and return number of lines. 
        self.__sd_toggle()
        try:
            f = open(self.file_path + self.file_name,"r") 
            x = f.readlines()
            datalines = len(x)
            f.close()
        except Exception as e:
            #file does not exist, create it
            f = open(self.file_path + self.file_name,"a")
            f.close()
            datalines = 0
        finally:
            self.__sd_toggle()
            return datalines

    def delete_arc(self, keep=0):
        #delete all archives with number lower than keep
        #try:
            tmp = self.file_name_archive
            arcs_present = self.get_arc() - 1 #get number of last archive
            if arcs_present < 2: return
            if keep >= arcs_present: keep = 0
            if keep > 0: arcs_present = arcs_present - keep + 1
            for x in range(1, arcs_present):
                tmp1 = self.file_name_archive + str(x) + '.txt'
                latest_archive = x
                try:
                    os.remove(self.arc_path + tmp1)
                    print(f'remove {self.arc_path}{tmp1}')
                except:
                    pass
            #now rename archives 1,2,3 etc
            filelist = os.listdir(self.arc_path)
            archive = []
            for eachfile in filelist:
                if eachfile.find(self.file_name_archive) > -1:
                    arc_number = self.__get_num(eachfile)
                    if arc_number > latest_archive: archive.append(eachfile)
            archive.sort()
            c = 0
            for x in archive:
                c += 1
            arc_number = 1
            for z in range(c):
                #print(f'rename {self.arc_path}{archive[z]}, {self.arc_path}{self.file_name_archive}{arc_number}.txt')
                os.rename(self.arc_path + archive[z], self.arc_path + tmp  + str(arc_number) + '.txt')
                arc_number += 1
        #except Exception as e:
            #print(str(e) + ' in delete_arc')
    
    def get_arc(self) :
        #return the next archive index for file, or 1 if file not yet archived.
        try:
            filelist = os.listdir(self.arc_path)
            arclist=[]
            arc = 1
            tmp = self.file_name[:len(self.file_name)-4] #filename without extension
            for x in filelist:
                file_stats = os.stat(self.arc_path + x)
                if file_stats[0] == 32768:
                    tmp1 = tmp + '_archive'
                    if x.find(tmp1) != -1:
                        tmp2 = x[:len(x)-4] #name with .txt removed
                        arclist.append (int(x[len(tmp1):len(x)-4]))
                        arc += 1
            if arc > 2:
                arclist.sort(reverse = True)
                arc = arclist[0] + 1
            return arc
        except Exception as e:
            print(str(e) + ' in get_arc')
            
    def check_size(self):
        #check log file size, and if it exceeds parameter rename it and create a new logfile
        if self.file_max_size == 0: return
        self.__sd_toggle()
        try:
            file_stats = os.stat(self.file_path + self.file_name)
            size = file_stats[6]
            if size > self.file_max_size:
                #get archive number of file if an archive already exists.
                #print(f'Archive: {self.file_name} size = {size} and max size = {self.file_max_size}')
                arc = self.get_arc()               
                #if saving to different volume, cannot rename, must save and delete
                #as os does not have a move or copy method
                if self.file_path == self.arc_path:
                    #print(f'Rename {self.file_name}, {self.file_name_archive}{arc}.txt')
                    os.rename(self.file_path + self.file_name, self.arc_path + self.file_name_archive + str(arc) + '.txt')
                else:
                    print(f'copy file to {self.arc_path}')
                    copy = self.copyfile(self.file_name_archive + str(arc) + '.txt')
                    if copy: os.remove(self.file_path + self.file_name)
                self.__sd_toggle()
                self.is_exist()
        except Exception as e:
            print(str(e) + ' in check_size')
        finally:    
            self.__sd_toggle()
    
    def copyfile(self, new_name, relocate=False):
        copy = True
        tmp = self.read()
        if self.arc_path == 'sd/': self.__sd_toggle()
        try:
            f=open(self.arc_path + new_name, 'w')
            f.write(tmp)
            f.close()
        except:
            copy = False
        if self.file_path == 'sd/': self.__sd_toggle()
        return copy
    
    def write(self, data):
        #ensure file exists, write data to file
        #create new file if it now exceeds max size
        self.__sd_toggle()
        self.is_exist()
        try:
            f = open(self.file_path +  self.file_name,"a")
            f.write(data + '\n')
            f.flush()
        except Exception as e:
            print(str(e) + ' in write')
        finally:    
            f.close()
            self.__sd_toggle()
            self.check_size()

    def read(self):
        self.__sd_toggle()
        text = """"""
        try:
            f = open(self.file_path + self.file_name,"r") #if except, file does not exist
            datalines = len(f.readlines())
            f.seek(0,0)
            for x in range(datalines):
                text += f.readline()
            f.close()
        except Exception as e:
            print(str(e) + ' in read.  ')
        finally:
            self.__sd_toggle()
            return text
    
    def delete(self):
        self.__sd_toggle()
        try:
            os.remove(self.file_path +  self.file_name)
            #print(self.file_path + self.file_name + ' removed')
        except:
            print(self.file_path +  self.file_name + 'does not exist')
        finally:
            self.__sd_toggle()
    
    def list_files(self, txt=False):
        self.__sd_toggle()
        try:
            print('Size\t Filename')
            filelist = os.listdir(self.file_path)
            for x in filelist: 
                tab = ' '
                if x != 'System Volume Information':
                    file_stats = os.stat(self.file_path + x)
                    size = file_stats[6]
                    if txt:
                        print(f'{size}\t {x}')
                    else:
                        if x[len(x)-3:] == 'txt':
                            print(f'{size}\t {x}')
                if (len(filelist)==1):
                    print('No files on card')
        except Exception as e:
            print(str(e) + ' in list_files')
        finally:
            self.__sd_toggle()
            return

    def Start_SD(self, sdi_pins):
        try:
            if self.pwr > 1: self.sd_pwr.value(1) 
            print('Initialize and mount the SD card')
            spi=SoftSPI(sdi_pins[0],sck=Pin(sdi_pins[1]),mosi=Pin(sdi_pins[2]),miso=Pin(sdi_pins[3]))
            sd=sdcard.SDCard(spi,Pin(sdi_pins[4]))
            # Create a instance of MicroPython Unix-like Virtual File System (VFS),
            vfs=os.VfsFat(sd)
            # Mount the SD card
            os.mount(sd,'/sd')
            if self.pwr > 0: self.sd_pwr.value(0)
            return True
        except Exception as e:
            print(str(e) + ' in Start_SD')
            if self.pwr > 1: self.sd_pwr.value(0) 
            return False
    
    def __sd_toggle(self):
        if self.SD:
            if self.sd_pwr.value() == 0: self.sd_pwr.value(1)
            if self.sd_pwr.value() == 1: self.sd_pwr.value(0)
    
    def __get_num(self, string):
        tmp = ''
        for i in string:
            if i.isdigit(): tmp += i
        return int(tmp)

class fm(fm_init_sd):
     def __init__(self, file_name, file_max_size=0, sd=False, bksd=False):
        super().__init__()
        self.file_path = '../'
        self.arc_path = '../'
        if sd:
            self.file_path = 'sd/'
            self.arc_path = 'sd/'
        if bksd:
            self.arc_path = 'sd/'
        self.file_name = file_name + '.txt'
        self.file_name_archive = file_name + '_archive'
        self.file_max_size = file_max_size
