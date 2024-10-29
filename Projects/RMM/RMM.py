"""
Copyright (c) 2024 David Flory  contact@moonlight-systems.co.uk

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
THE SOFTWARE

"""
class rtc_mem:
    def __init__(self, limit):
        self.__assets = {}
        self.__types = [int,float,bool,bytearray,str,list,tuple,set,dict]
        self.__recode = ''
        self.__code = "data = ''\nf = open('var.txt','r')\ndata = f.read()\nf.close()\nexec(data)\n"
        self.__limit = limit
        self.debug = False
        
    def preserve(self, ob,nm):
        tp = 10
        for x in range(9):
            if ob == self.__types[x]:
                tp = x
                if tp < 9:
                    self.__assets[nm] = self.__types[x]
        if tp == 10:
            if self.debug:
                print(type(ob),end=" ")
                print(' is not supported.')
            return
    
    def save(self):
        return self.__assets
    
    def parse(self, z, x):
        if x == 'end':
            size = len(self.__recode)
            if self.debug:
                print('save data = ',end=" ")
                print(size,end=". ")
            if size > self.__limit:
                if self.debug: print('Writing to file.')
                f = open('var.txt','w')
                f.write(self.__recode)
                f.close()
                return self.__code
            print()
            return self.__recode
        y = type(z)
        if y == str:
            safe = z.replace('\n',' ') #remove newline character if present.
            self.__recode += x + " = '" + safe +"'" +'\n'    
        elif y == int:
                self.__recode += x + " = " + str(z) + "\n"           
        elif y == float:
                self.__recode += x + " = " +str(z) + "\n"
        elif y == tuple:
            size = len(z)
            if size > 0:
                var = "("
                for item in range(size):
                    if type(z[item]) == str: var += "'" + z[item] + "'"
                    elif type(z[item]) == int or type(z[item]) == float or type(z[item]) == bool: var += str(z[item])
                    if item < size -1: var += ','
                var += ")"   
                self.__recode += x + "=" + var+"\n"
        elif y == list or y == set:
            if len(z) > 0:
                var = "["
                for item in z:
                    if type(item) == str: var += "'" + item + "',"
                    elif type(item) == int or type(item) == float or type(item) == bool: var += str(item) + ","
                var = var[:len(var)-1] + "]"
                self.__recode += x + "=" + var+"\n"  
        elif y == dict:
            pass  
        elif y == bool:
            self.__recode += x + " = " +str(z) + "\n"
        elif y == bytearray:
            pass
        else:
            pass
        