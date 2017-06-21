**Raw LoRa**: Sending and receiving messages between two nodes

# Raw LoRa (LoRa-MAC)

## Introduction
In this example, we will **establish a connection between two Lopy nodes in LoRa-MAC mode**, and bypass the LoRaWAN layer (can be mapped to the second and third layer of the OSI model). 

## Learning outcomes

You will learn how to:
* establish a connection between two nodes in LoRa-MAC mode
* setup a basic channel access control mechanisms

## Required Components

For this example you will need:

- a LoPy or WiPy module
- a microUSB cable
- a development PC

The source code is in the `src/lora-mac` directory.

## Code

### boot.py
```python
from machine import UART
import os
uart = UART(0, 115200)
os.dupterm(uart)
```

The boot.py file should always start with the above code, so we can run our python scripts over Serial or Telnet. Newer Pycom boards have this code already in the boot.py file.

### main.py
```python
from network import LoRa
import socket
import machine
import time

# Name of your team
team_name = 'your team name'

# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

while True:
    # send some data
    s.setblocking(True)
    s.send('Hello from {}'.format(team_name))

    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)
```

Let's go through the code above:

```python
from network import LoRa
import socket
import machine
import time
```
First, we import the required modules, the new ones here being:

* [LoRa (class providing a driver for the LoRa network processor in the LoPy)](https://docs.pycom.io/pycom_esp32/library/network.LoRa.html)
* [socket (providing access to the BSD socket interface.)](https://docs.pycom.io/pycom_esp32/library/usocket.html)


```python
# We create and configure a LoRa object
lora = LoRa(mode=LoRa.LORA)
```
Mode can be either `LoRa.LORA` or `LoRa.LORAWAN`. Please refer to the [LoRa class documentation](https://docs.pycom.io/pycom_esp32/library/network.LoRa.html) to look at the multiple parameters we can pass (will cover some of them in the exercises).


```python
# We open a socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
```
passing `socket.AF_LORA` as family type, and `socket.SOCK_RAW` as socket type.


```python
while True:
    # send some data
    s.setblocking(True)
    s.send('Hello from {}'.format(team_name))

    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)
```
Then, we repeatedly send and listen for data through the socket:
1. put the socket in blocking mode as we are about to send data
2. send the data
3. "unblock" the socket as we are now about to listen to data received
4. read data from the socket (here buffer size is 64 bits)
5. and finally, wait a random amout of time (betwee 0 and 15s - 0x0F)




## Exercises
1. Identify the MAC addresses of your Lopy nodes and use them to filter out messages received (yours only).
2. Find out how to change specific raw LoRa parameters to setup a basic channel access control mechanisms.