from utime import localtime, mktime, gmtime


year = int(input('Enter current year in four digit format: '))
month = int(input('Enter month this year clocks will go [or went] forward: '))
day = int(input('Enter day this year clocks will go [or went] forward: ' ))
spring = (year,month,day)
month = int(input('Enter month this year clocks will go [or went] back: '))
day = int(input('Enter day this year clocks will go [or went] back: '))
autumn = (year,month,day)
hs = int(input('Enter 1 for northern hemisphere, 0 for Southern hemisphere: '))
hemisphere = True
print()
if hs == 0: hemisphere = False

if hemisphere:
    #get yeardays for EU
    dts = (2024, 3, 31,10,0,0,0,0)
    epoch = mktime(dts)
    yds1 = (localtime(epoch)[7])
    dta = (2024, 10, 27,10,0,0,0,0)
    epoch = mktime(dta)
    yda1 = (localtime(epoch)[7])

    dts = (2024, 4, 26,10,0,0,0,0)
    epoch = mktime(dts)
    yds2 = (localtime(epoch)[7])
    dta = (2024, 10, 31,10,0,0,0,0)
    epoch = mktime(dta)
    yda2 = (localtime(epoch)[7])


    print('Yeardays for UK are ',end=" ")
    print(str(yds1) + ' and ' + str(yda1))
    print('Yeardays for USER are ',end=" ")
    print(str(yds2) + ' and ' + str(yda2))

    offset1 = yds2 - yds1
    offset2 = yda2 - yda1

    print ('Offset for spring is ' + str(offset1) + ' and Autumn is ' + str(offset2))
else:
    #get yeardays for AUS
    dts = (2024, 10, 6,10,0,0,0,0)
    epoch = mktime(dts)
    yds1 = (localtime(epoch)[7])
    dta = (2024, 4, 7,10,0,0,0,0)
    epoch = mktime(dta)
    yda1 = (localtime(epoch)[7])
    
    dts = (2024, 9, 29,10,0,0,0,0)
    epoch = mktime(dts)
    yds2 = (localtime(epoch)[7])
    dta = (2024, 4, 7,10,0,0,0,0)
    epoch = mktime(dta)
    yda2 = (localtime(epoch)[7])


    print('Yeardays for AUS are ',end=" ")
    print(str(yds1) + ' and ' + str(yda1))
    print('Yeardays for USER are ',end=" ")
    print(str(yds2) + ' and ' + str(yda2))

    offset1 = yds2 - yds1
    offset2 = yda2 - yda1

    print ('Offset for spring is ' + str(offset1) + ' and Autumn is ' + str(offset2))
print()
info = """Make the following edits in the TSYNC.py code under the line "elif self.country == 'USER"
which is in the function "def get_DST(self):" There are 2 sections, Spring and Autumn, and each of those
has a section for Northern hemisphere and Southern hemisphere.
Change the line "offset_days = 0" in either North or South hemispheres as required to
offset_days = """ 
print(info + str(offset1) + ' for Spring, and offset_days = ' + str(offset2) + ' for Autumn.')