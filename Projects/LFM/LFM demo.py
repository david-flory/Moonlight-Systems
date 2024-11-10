import LFM

#If you have an SD card attached, call  LFM.fm_init_sd with
#your SPI pin numbers as a tuple with six elements, in the orderof 
#slot number, sck, miso, mosi, and cs. The last parameter is 0 if your
#SD Card breakout is permanently powered, or the pin number that
#provides power when you turn in on and off.
lfm = LFM.fm_init_sd((2,5,32,14,27,0))
#This variable used to toggle between SD card files and files saved to ESP flash.
SD = lfm.is_sd()

#If you are not using an SD Card, there is no need to initialise the library
#or create the 'SD' variable.

#For each file you want to create, initialise an instance of the file name
#The first parameter is the file name without an extention, it will be suffixed with '.txt'
#The second parameter is optional, and is the maximumum size you want to set for the file.
#If included, when the file size is greater than this figure, it is renamed
#filename_archive.txt and a new filename.txt created.

#This creates files on the ESP flash
data_log=LFM.fm('data_log', 0)
print('Filename: ' + data_log.file_name)
print('File Max size set to: ' + str(data_log.file_max_size))

#If an SD card is present, use a 3rd parameter, the variable 'SD'
#to denote the file is to be written to the SD card.

serial_log=LFM.fm('serial_log', 150,SD)
print()

print('Filename: ' + serial_log.file_name)
print('File Max size set to: ' + str(serial_log.file_max_size))
print('When file reaches max size it will be renamed to ' + serial_log.file_name_archive)

"""
There is also another option when creating the file instance.
If you have an SD card installed, and want to save the file to the ESP main filesystem
but want the archives backed up on the SD card, use an optional parameter 'bksd=SD'
where SD is the boolean variable created when initialising the SD card. Though you could use 'bksd=True'
if the initialisation of the card failed and returned false, an error will be raised when trying to write an archive to it.

serial_log=LFM.fm('serial_log', 150, bksd=SD)
"""

#to write to the files use the file's write() function
data_log.write('Writing something to data_log')
serial_log.write('Writing something serial_log')

#To read from files use the file's read() method

print('data_log file contents:')
print(data_log.read())

print()
print('serial_log file contents:')
print(serial_log.read())

#to list files use the list_files() method on any file instance that is using the filesystem you want to list
print('Files on card.')
serial_log.list_files()
print()
print('Files on ESP.')
data_log.list_files()
print()

#To delete a file, use the file's delete() method
#serial_log.delete()
#data_log.delete()

#To delete archived files, use the file's delete_arc() method
#param is optional. If used, it will be the number of archives to remain.
#These will be the latest archives and renumbered 1, 2, 3 etc with oldest first.
#If empty it defaults to 1 so all archives except the latest will be deleted, and
#that archive will be renumbered to 1

#serial_log.delete_arc(3)