**Persisting data**: Writing data on `/flash` or `/SD` card in a LoPy device.

# Persisting data

## Introduction
While one of the primary purpose of IoT is to collect and exchange data over an inter-connected network, it is as well important to be able to persist information in the IoT device itself: log files of device's activity, Received Signal Strength Activity (RSSI), ...

## Learning outcomes
You will learn how to:
* access and operate device's file system;
* create and write a file in the `flash` folder;
* mount and use an `SD` card as an alternative;
* handle files safely using `with` statement;
* generate programmatically time stamped log file names;
* make your code robust and flexible with `try ... except` statement.

## Required Components

For this example you will need:

- a LoPy or WiPy module
- a microUSB cable
- a development PC

The source code is in the `src/micro-sd` directory.

## Folder structure
The folder tree is the following:

```
/ (root)

    /flash
        main.py
        boot.py
       /lib
       /cert
       /sys

    /sd (if mounted)
```

By default, when you sync `main.py, boot.py, ...` from your atom project, these files are written into the `flash` folder.

Let's explore and navigate this folder structure interactively. Connect to a Lopy via the Atom console and import the [basic operating system module (os)](https://docs.pycom.io/pycom_esp32/library/uos.html): `import os`. 

Once imported:
* to know you current working directory: `os.getcwd()` (most probably the `/flash`folder);
* to list folders and files in your current working directory: `os.listdir()``;
* to create a new folder/directory named "log": `os.mkdir('log')`;
* ... 

Take a look at [os module documentation](https://docs.pycom.io/pycom_esp32/library/uos.html) for a full list of methods.

Now notice that if you list the files and folders under the `root` folder:
`os.listdir('/'),`you get only the `flash` directory. There is no `SD` card mounted yet.

## Writing 
In the simplest case, to create and write a new file:

```python
os.listdir('/flash')

# create/open, write, close a file
f = open('log/my_first_file.log', 'w')
f.write('Testing write operations in a file.')
f.close()

# open, read, close an existing file
f = open('log/my_first_file.log', 'r')
f.readall()
f.close()
```
For further reference on reading and writing files in Python, look at the official documentation [here](https://docs.python.org/3.4/tutorial/inputoutput.html). 

But in essence to handle files in Python, you first need to open a file (even if it does not exist yet)
```python
f = open('log/my_first_file.log', 'w')
```
the `open` function takes as argument:
* file name `'log/my_first_file.log'` (relative or full path)
* and mode: read, write, ...

Once open, you get a file object to play with and hence can start writing data in it:
```python
f.write('Testing write operations in a file.')
```

Then you need to close the file to free up any system resources taken up by the open file. After calling `f.close()`, attempts to use the file object will automatically fail.

**Pro tip**: using the `with` statement.

It is good practice to use the `with` keyword when dealing with file objects. This has the advantage that the file is **properly closed after its suite finishes, even if an exception is raised on the way**. It is also much shorter than writing equivalent try-finally blocks. 

For instance to read the file just created, you can use the following syntax:

```python
with open('log/my_first_file.log', 'r') as f:
    f.readall()
```

This is much cleaner and safer. 

Finally, before creating a folder or a file, we would like to test if it exists already. The code below test it and recap. the whole process:

main.py under `src/micro-sd/flash` directory:
```python
import os
file_path = '/flash/log'

try:
    os.listdir('/flash/log')
    print('/flash/log file already exists.')
except OSError:
    print('/flash/log file does not exist. Creating it ...')
    os.mkdir('/flash/log')

name = '/my_first_file.log'

# Writing
with open(file_path + name, 'w') as f:
    f.write('Testing write operations in a file.')

# Reading
with open(file_path + name, 'r') as f:
    print(f.readall())
```

The `try ... except` statement does the following:
1. **try** to list the files and folder under `/flash/log` folder;
2. if the folder does not exist an error occurs (it raises an OSError **except**ion) that we intercepts to write our message and create our folder.

## Mounting an SD card
An SD card (Secure Digital) is a non-volatile memory card format for use in portable devices. Secure Digital includes four card families available in three different sizes (refer to [SD card wikipedia entry for further information](https://en.wikipedia.org/wiki/Secure_Digital)).

The Pycom expansion board accepts the micro SD size formatted as `FAT16`or `FAT32` ([FAT file system architecture](https://en.wikipedia.org/wiki/File_Allocation_Table)). A file system is used to control how data is stored and retrieved. There are many of them for instance: NTFS (Windows), HFS (mac OS), ... **The family of FAT file systems is supported by almost all operating systems for personal computers** hence its relevance here.

To use an `SD card`:
* insert your SD card in expansion board (see picture below)

![lopy-expansion-board-sd.png](http://i.imgur.com/9WYmnLr.jpg?2)

2. then write the following code line by line in Atom console:

```python
from machine import SD
import os

sd = SD()
os.mount(sd, '/sd')

# check that you have now two folders under root directory
os.listdir('/')

# try some standard file operations
f = open('/sd/test.txt', 'w')
f.write('Testing SD card write operations')
f.close()

f = open('/sd/test.txt', 'r')
f.readall()
f.close()
```

Now, a bit of code refactoring in main.py under `src/micro-sd/sd` folder:

```python
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
```


## "Advanced" code [optional]
When we use log files to monitor a device's activity, we often want to generate programmatically a file name in the following format:
`/flash/log/acq/yyyymmddhhmmsslist.csv` with:
* `yyyy` current year;
* `mm` current month;
* ...

A first simple, explicit and readable approach could be:
```python
import time 

year, month, day, hour, minute, second, ms, dayinyear = time.localtime()

nameCsv = '/flash/log/acq'
nameCsv = nameCsv + '{:04d}'.format(year)
nameCsv = nameCsv + '{:02d}'.format(month)
nameCsv = nameCsv + '{:02d}'.format(day)
nameCsv = nameCsv + '{:02d}'.format(hour)
nameCsv = nameCsv + '{:02d}'.format(minute)
nameCsv = nameCsv + '{:02d}'.format(second)
nameCsv = nameCsv + 'list.csv'
```
A second approach more succinct would be to take advantage of Python list comprehensions:

```python
base = '/flash/log/acq/'
time_stamp = ''.join(['{:02d}'.format(i) for i in time.localtime()][:6])
name = base + time_stamp + 'list.csv'
````

Let's unpack this second implementation:

* **local time**
```python
time.localtime()
```
outputs a tuple `(1970, 1, 1, 0, 21, 40, 3, 1)` representing year, month, ...

* **formatting integer to string with list comprehension**
```python
['{:02d}'.format(i) for i in time.localtime()]
```
outputs `['1970', '01', '01', '00', '24', '05', '03', '01']`

We keep only year, month, day, hour, min., sec. by slicing the list:
```python
['{:02d}'.format(i) for i in time.localtime()][:6]
```

* **last we join the list to a single string**
```python
''.join(['{:02d}'.format(i) for i in time.localtime()][:6])
```
outputs: `'19700101002920'`

We can now simply concatenate this substring with a prefix and suffix and that's done.

As it is a quite frequent operation, we could even encapsulate it in an helper function as below:

```python
def get_log_filename(prefix, suffix):
    time_stamp = ''.join(['{:02d}'.format(i) for i in time.localtime()][:6])
    return prefix + time_stamp + suffix
```

and use it when required: `get_log_filename('/flash/log/acq', 'list.csv')`

## Exercise
Write a script writing a file named `"log.csv"` in `/flash/log/` folder so that:
* if the user pushes the button the pressing time and an incremented counter is saved;
* it the counter reaches 10, LED is switched on.
