**LED**: "Hello, world" in the IoT World

# LED

## Introduction

In this example, we will create and deploy the proverbial 1st app, “Hello, world!” to a Pycom device. Because the board does not have a display, we will use the USB connection between the board and the development PC to switch on and off an LED. In the simplest terms, a Light-Emitting Diode (LED) is a semiconductor device that emits light when an electric current is passed through it. LEDs are described as solid-state devices. The term solid-state lighting distinguishes this lighting technology from other sources that use heated filaments (incandescent and tungsten halogen lamps) or gas discharge (fluorescent lamps). Different semiconductor materials produce different colors of light. 


The LoPy module has one LED as shown on the top in this picture.

![](http://i.imgur.com/K7lEu24.png)

The pycom expansion board has also a (smaller) LED shown on the right in the picture. We will use the LED of the LoPy module and will refer to this as the LED.


## Learning outcomes

You will learn how to:
* switch on and off the LED;
* pause the execution of the code for a certain amount of time.

## Required Components

For this example you will need:

* a LoPy or WiPy module
* a microUSB cable

The source code is in the `src/LED` directory.

> Activating the LED consumes a lot of energy. Make sure you don't use LEDs if you want to have a low power system.

## Code

Let's first operate the LED using the terminal interface. From the command line, enter:

```python
import pycom
pycom.heartbeat(False) 
pycom.rgbled(0xFF0000) 
```

The first line tells the system that you will use the pycom library. This library includes the utilities necessary to operate the specific pycom hardware.
The second line tells the system NOT to use the heartbeat functionality of the LED. In normal operations, the LED will blink with a blue color every second to show that the device is running properly.
The third line tells the system to switch on the LED with a xxx color. The color code is the following (with the first six characters showing the Red Green Blue components, in exadecimal format):

* blue is `0x00007f`
* red is `0x7f0000`
* green is `0x007f00`
* yellow is `0x7f7f00`

If you now disconnect the USB cable, the device will reset and the LED will go back to defult state (heartbeat mode).

If you want your code to be permanently stored on the board, you need to open the LED directory and sync it to your board.
### boot.py

```python
from machine import UART
import os
uart = UART(0, 115200)
os.dupterm(uart)
```
The boot.py file should always start with following code, so we can run our python scripts over Serial or Telnet. Newer Pycom boards have this code already in the boot.py file.

For instance in our case, it allows to run Python single expressions or scripts via the console. Such console is called a **REPL** (Read Print Eval Loop). Simply put, it takes user inputs, evaluates them and returns the result to the user.

* line 1: we import from the [`machine` module](https://docs.pycom.io/pycom_esp32/library/machine.html) the class `UART` (duplex serial communication bus)
* line 2: we import the [`os` module](https://docs.pycom.io/pycom_esp32/library/uos.html) (basic operating system services)
* line 3: we create an UART object (initalized with `bus number=0` and `baudrate=115200` - the clock rate)
* and finally pass it to the `dupterm` method of the os module in order to make the REPL possible via **Atom editor** for instance.

### main.py

```python
import pycom
import time
pycom.heartbeat(False)
for cycles in range(10): # stop after 10 cycles
    pycom.rgbled(0x007f00) # green
    time.sleep(5)
    pycom.rgbled(0x7f7f00) # yellow
    time.sleep(5)
    pycom.rgbled(0x7f0000) # red
    time.sleep(5)
```

You should see the LED light up for five seconds at a time, in green, yellow and red. After the sequence has gone through ten cycles, the system will stop and the LED will remain red.

Let's analyze the code:

```python
import pycom
import time
```

We first import two libraries: pycom and time. The pycom one includes the utilities necessary to operate the specific pycom hardware. The time one is used to keep track of time and helps operate the internal clock.

```python
pycom.heartbeat(False)
```

We then deactive the heartbeat funcionality.

```python
for cycles in range(10): # stop after 10 cycles
```

We start a cycle and limit it to 10.


> Indentation is very important in python! Make sure you indent the code after the `for` command.


```python
    pycom.rgbled(0x007f00) # green
    time.sleep(5)
```

Switch on the LED and select the green color. Then sleep for 5 seconds. The sleep command accepts seconds (and not milliseconds not minutes!).

## Exercises

1. Try to send an SOS message using the LED. The SOS is ---...--- in morse code, where a line is three times longer than a dot.

2. Find out how short can the sleep be, while still having a blinking LED (and not a fixed one).
