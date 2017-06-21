**Utilities**: connecting to a WiFi network

# Utilities

## Introduction

As you know the popularity of WiFi has grown steadily in the last decade. WiFi allows local area networks (LANs) to operate without cables and wiring, making it a popular and cost-effective choice for home, business and research networks. Some cities have even constructed free citywide WiFi networks. Using WiFi, IoT nodes can make use of the existing network infrastructure to send data over the Internet.

In the following examples, we will learn how to connect to a WiFi network, how to measure the signal strength, how to read data from a webpage to get the correct time and how to find out the latest weather status.

>The Pycom modules WiPy and LoPy both have WiFi capabilities. You don't need the expansion board to use the WiFi capabilities.

Pycom modules can act as **Access Point** and as **Client**. An Access Point (AP) is a networking hardware device that allows a WiFi compliant device to join a network. You can use your laptop/smarthphone/tablet to connect to a Pycom module running as AP. If your module is setup as a WiFi client, it can join an Access Point and connect to the Internet (or any IP network).  

Most countries have only a limited number of frequencies legally available for use by wireless networks. Usually, adjacent Access Points will use different channels to communicate with their clients in order to avoid interference between two nearby systems. The limited number of channels becomes problematic in crowded areas with multiple APs. In such an environment, signal overlap becomes an issue causing interference, which results in signal droppage and data errors.

Wireless access requires special security considerations. Wired networks base the security on physical access control, trusting all the users on the local network, but if APs are connected to the network, anybody within range of the AP can attach to the network. The most common solution is wireless traffic encryption. Modern access points come with built-in encryption. WPA and WPA2, are considered secure if a strong enough password or passphrase is used.

In the examples we will use NTP to sync the module's clock. Why do we want to have a have a precise clock on an IoT module? Isolated devices may run their own wrong time, but as soon as they connect to the Internet or they work together with other devices, effects will be visible. Just imagine three devices measuring temperature in an apartment. If their clocks are not synchronized, the readings will not be useful to take decisions about operating an AC.  

NTP stands for Network Time Protocol, and it is an Internet protocol used to synchronize the clocks of computers to some time reference. The protocol is highly accurate, using a resolution of less than a nanosecond (about 2^-32 seconds). There are more than 100,000 hosts running NTP in the Internet. 


## Learning outcomes

You will learn how to:
* connect to an Access Point with WPA authentication;
* connect to an open Access Point;
* measure the received signal level (RSSI) and the Signal to Noise Ratio (SNR);
* sync the module's clock with an online clock service using NTP.

## Required Components

For this example you will need:

* a LoPy or WiPy module
* a microUSB cable
* a development PC

The source code is in the WiFi directory.


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

For instance, in our case, it allows to run Python single expressions or scripts via the console. Such console is called a **REPL** (Read Print Eval Loop). Simply put, it takes user inputs, evaluates them and returns the result to the user.

* line 1: we import from the [`machine` module](https://docs.pycom.io/pycom_esp32/library/machine.html) the class `UART` (duplex serial communication bus)
* line 2: we import the [`os` module](https://docs.pycom.io/pycom_esp32/library/uos.html) (basic operating system services)
* line 3: we create an UART object (initalized with `bus number=0` and `baudrate=115200` - the clock rate)
* and finally pass it to the `dupterm` method of the os module in order to make the REPL possible via **Atom editor** for instance.


## Connect to an Access Point with WPA authentication

In this example we will connect to an Access Point called "MyAP" with password "MyPassword" using WPA authentication.

### main.py

```python
import machine
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'MyAP':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'MyPassword'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

```

You should see the following messages in the terminal window:

```
Network found!
Wifi: connected with MyAP, channel 11
WLAN connection succeeded!
```

Let's analyze the code:

```python
import machine
from network import WLAN
```

We first import two libraries: machine and WLAN. The machine one includes the utilities needed to XXX. The WLAN library is used to retrieve the current WLAN instance.

```python
wlan = WLAN(mode=WLAN.STA)
```

We then set the WiFi mode to client (which is technically called Station Mode, therefore we use STA).


```python
nets = wlan.scan()
```

We scan for all available WiFi networks. If you call the "wlan.scan()" command in the terminal, you will see a list of all available WiFi networks in your area. In this example, we save this list in the nets variable.


```python
for net in nets:
    if net.ssid == 'MyAP':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'MyPassword'), timeout=5000)
```

Let's check all the networks' ssid (this is the technical name for the Access Point's name, such as MyAP or MainLibrary or LabWifi, etc) and see if any of them correspons to "MyAP". If so, print "Network found!" and connect to it using the password "MyPassword". 

```python
while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
```

Continue checking all the AP names in the variable "net". If you are still not connected, please go in power saving mode. If you are connected, print "WLAN connection succeeded!" and exit from the cycle. 


## Connect to an Access Point with WPA authentication, store credentials in a separate file and show network information


In this example we will connect to an Access Point called "MyAP" with password "MyPassword" using WPA authentication. For very simple tasks you might choose to write these configuration variables directly into the source code. But this is a bad idea when you upload the code to GitHub or share it with someone on the Internet. We will store the WiFi credentials in a separate file called config.py and in the main.py we will  show the network information (IP address, etc) once connected to the network. 


## config.py

```python
ssid = 'MyAP'
password = 'MyPassword'
```

The configuration file contains only the name (SSID) of the network and the password.


### main.py


```python
import machine
import config
from network import WLAN
wlan = WLAN(mode=WLAN.STA, antenna=WLAN.INT_ANT)

nets = wlan.scan()
for net in nets:
    if net.ssid == config.ssid:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, config.password), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

print(wlan.ifconfig())
```

You should see the following messages in the terminal window:

```
WLAN connection succeeded!                        
('10.0.1.12', '255.255.255.0', '10.0.1.1', '10.0.1.1') 
```
Let’s analyze the new lines in this example:

```python
import config
```
We import the configuration file containing the Access Point name and the password.

```python
wlan = WLAN(mode=WLAN.STA,antenna=WLAN.INT_ANT)
```
Antenna selects between the internal and the external antenna. It can be either WLAN.INT_ANT or WLAN.EXT_ANT. 

XXXX- PICTURE OF ANTENNA CONNECTORS OF LOPY AND WIPY

## Connect to an Access Point with WPA authentication, store credentials in a separate file and show network information

In this example we will connect to an Access Point called "MyAP" which is open and does not require any password.


## Exercises

1. Try to send an SOS message using the LED. The SOS is ---...--- in morse code, where a line is three times longer than a dot.

2. Find out  what is the shortest sleep interval that will still keep the  LED blinking (NOT permanently on).
