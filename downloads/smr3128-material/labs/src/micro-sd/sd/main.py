from machine import SD
import os

sd = SD()

# mount SD if not mounted already
try:
    os.mount(sd, '/sd')
except OSError:
    print("SD card already mounted.")
    pass

# create 'log' folder if does not exist
try:
    os.listdir('/sd/log')
    print('/sd/log file already exists.')
except OSError:
    print('/sd/log file does not exist. Creating it ...')
    os.mkdir('/sd/log')

file_path = '/sd/log'
name = '/my_second_file.log'

# Writing
with open(file_path + name, 'w') as f:
    f.write('Testing write operations in a file.')

# Reading
with open(file_path + name, 'r') as f:
    print(f.readall())
