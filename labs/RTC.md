RTC (setting the clock, timers)

# RTC

## Introduction

In this example we will demonstrate how to manually set and read time in the Real Time Clock of the pycom module.

Most microcontrollers, including the pycom modules, have a built-in clock and there are also timers built into the module that can keep track of longer time periods like minutes or days. This clock only keeps track of time since the device was last powered. That means that when the power is turned on, the timer is set back to 0. The module doesn't know the month, day, year or time. It can only tell it's been a certain amount of milliseconds since I was last turned on.

If you want to set the time on the pycom module, you have to program  the date and time and you could have it count from that point on. But if it lost power, you'd have to reset the time. 

Some projects such as data-loggers (where data is time-stamped accurately) need to have consistent timekeeping that doesn't reset when the  battery dies. In this case, you have to add a separate RTC module connected to the module.

In these examples,we will only use the internal clock, so keep the module powered via USB or via a battery.

## Learning outcomes

You will learn how to:
* read the time;
* set the time.

## Required Components

For this example you will need:

* a LoPy or WiPy module
* a microUSB cable
* a development PC

The source code of the examples are in the RTC directory.


## Code

The following example codes use the same boot.py


### boot.py
```python
from machine import UART
import os
uart = UART(0, 115200)
os.dupterm(uart)
```
The boot.py file should always start with the above code, so we can run our python scripts over Serial or Telnet. Newer Pycom boards have this code already in the boot.py file.


## Read time

In this example we will read the current date and time.

### main.py

```python
from machine import RTC
rtc = RTC()
print(rtc.now())
```

We first initialize the RTC and then print the current date and time. The result will be something like:

```
(1970, 1, 1, 0, 0, 1, 51300, None)
```

As you will not be reading this document in 1970, the date is clearly wrong. 

## Set time

In this example we will manually set the current date and time.

```python
from machine import RTC
rtc = RTC()
# for 22nd of June 2017 at 10:30am (TZ 0)
rtc.init((2017, 6, 22, 10, 30, 0, 0, 0))
print(rtc.now())
```
The arguments when you initialize the RTC are a tuple of the form:

year, month, day, hour, minute, second, microsecond, tzinfo

tzinfo is ignored by this method. 
