**LoRa coverage**: collecting and mapping RSSI and SNR

# LoRa coverage

## Introduction
In this example, we want to produce a LoRA coverage map. The setup is the following:
* a fixed node will send messages over LoRa;
* on reception, a mobile node will:
    * determine **RSSI** (Receive Signal Strength Indicator) and **SNR** (Signal Noise Ratio) using messages received;
    * send query to an Android phone to get GPS coordinates.


## Learning outcomes

You will learn how to:
* produce a LoRa coverage map, and;
* use an Android phone as a GPS server.

## Required Components

For this example you will need:

- a LoPy module that will be used as a Transmitter (fixed position)
- a LoPy module that will be used as a Receiver (nomadic)
- an Android phone with `Shared GPS` application installed
- two microUSB cables
- a development PC

The source code is in the `src/lora-coverage` directory.

> Always update the firmware to the most recent version.

## 1. Android phone setup
The Android phone will be used as a **GPSD** (GPS Daemon) server responding to TCP queries. The mobile node will send TCP queries to the Android device and will get back GPS coordinates.

To set up such GPS Daemon on your Android device, you first need to install an application named "Share GPS" available here:  [https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS&hl=en](https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS&hl=en)

The full documentation of this app. is available here: [http://www.jillybunch.com/sharegps/user.html](http://www.jillybunch.com/sharegps/user.html)

Once installed, the first step is to enable your Android device as Wi-Fi Hotspot with the following parameters:
* **NAME**: `your_name`
* **WPA2 KEY**: `your_key`

We will now create a new connection:

1. Click on `ADD` button to create a new connection: 

![img/shared-gps-home.png](http://i.imgur.com/qrUpyQN.png)

2. Reproduce the following settings:

![img/shared-gps-settings-1.png](http://i.imgur.com/UbE0zpV.png)

3. Click `NEXT` and reproduce settings below and press `OK`:

![img/shared-gps-settings-2.png](http://i.imgur.com/WvGdVv3.png)

By now, you should have a "fresh" new connection listed under the `CONNECTIONS` tab:

![img/shared-gps-home-with-connex.png](http://i.imgur.com/nNGIoYQ.png)

* **To start the server**: click on the connection created (the blue `Idle` status should then turn to `Listening` in yellow).
* **To stop it**: Press and hold on the connection and press `Disconnect`.

Last, check that you have the following `Advanced settings`: click the three vertical dots on the top-right of the screen:

![img/shared-gps-advanced-settings-1.png](http://i.imgur.com/L9HxGp8.png)

![img/shared-gps-advanced-settings-2.png](http://i.imgur.com/iJJllzs.png)

Your GPSD server is now ready to use!

## 2. Transmitter node setup
The sole responsibility of the transmitter node is to send LoRa packets (in that specific case with minimal information in it - device's MAC address).

That way, the receiver, from receipt of the packet , will measure the **RSSI** and **SNR**. Indeed, there is a dedicated method in `LoRa class` named `lora.stats()` returning a named tuple with usefel information from the last received LoRa or LoRaWAN packet. The named tuple has the following form:

```
(rx_timestamp, rssi, snr, sftx, sfrx, sftx, tx_trials)
```
You can find the source code to be synchronized to your Lopy in the following folder `src/lora-coverage/lora-tx-node` including:
* `boot.py`
* `utils.py` and
* `main.py` (below)


```python
import network
from network import LoRa
import binascii
import socket
import machine
import time
import binascii
import sys
import utils # utilities module with CRC calculation

# Initialize LoRa in LORA mode.
lora = LoRa(mode=LoRa.LORA)

# Get loramac as id to be sent in message
lora_mac = binascii.hexlify(network.LoRa().mac()).decode('utf8')

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

count_tx = 0

# tx loop every 2s
while True:
    s.setblocking(True)

    # ConstBuild the message
    msgtx = str(count_tx) + ',' + lora_mac
    
    # Calculate CRC error detecting code
    crc8 = utils.crc(msgtx.encode('utf8'))
    
    # Add crc8 to message to be sent
    msgtx = msgtx + ',' + crc8
    
    # Send message
    s.send(msgtx)
    print('Tx: {} is sending data ...'.format(lora_mac))

    count_tx += 1

    # Get any data received...
    s.setblocking(False)
    data = s.recv(64)

    time.sleep(2)
```

## 3. Receiver node setup
The receiver will sequentially:

1. Read GPS coordinates from the Android device via TCP
2. Read `RSSI` and `SNR` from the last received LoRa packet
3. Log into a `.csv` file in the `flash/log/` folder `rssi, snr, time, lon, lat, CRC, ...`.

You can find the source code to be synchronized to your Lopy in the following folder `src/lora-coverage/lora-rx-node` including:
* `boot.py`
* `utils.py` and
* `main.py` (below)


## 4. Preparing data collection

1. Sync. relevant code to each nodes
2. Set your Android "ShareGPS" in `Listening` mode
3. Soft reboot receiver node
4. Start moving around with your receiver node + Android while your Transmitter stay in a fix position
5. Press the button on expansion board to stop the acquisition
6. Retrieve logged data via ftp (Filezilla)
7. Analyse and map data collected

## 5. Retrieving logged data from device's via ftp

See [workflow-and-setup.md](workflow-and-setup.md) lab tutorial to set up Filezilla ftp connection to a Pycom device.

## 6. A quick and dirty map in a Jupyter notebook
In `src/lora-coverage/notebooks` you will find a Jupyter notebook named `lora-coverage-map.ipynb`, open it with Anaconda Jupyter notebook using a `Python 2.7` kernel.

As you will notice in the notebook the following Python modules will be required:

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
from palettable.colorbrewer.sequential import YlGnBu_5_r

import geopandas as gpd
from shapely.geometry import Point

import mplleaflet

%matplotlib inline
```
Before running the notebooks, you need first to install them in your Anaconda environment.

This notebook shows how to:
* read a csv file
* assess the structure of a file (descriptive statistics, ...)
* perform basic EDA (Exploratory Data Analysis)
* create a "Quick & Dirty" LoRa coverage map for quick visual assessment.


## Exercises
1. Update `main.py` of receiver node to change the LED color to orange when `RSSI < -150 dB`

2. Form three teams. Each team will set up
    * a transmitter (at a fixed location of your choice)
    * 2 mobile nodes (receivers) 

LoRa network connections for both transmitters and receivers should be setup as follows:

| Team   | Spreading Factor      | Frequency (MHz)  |
| ------ |-----------------------| -----------------|
| 1      | 5                     | 863              |
| 2      | 7                     | 867              |
| 3      | 12                    | 870              |


Pycom LoRa class documentation; (https://docs.pycom.io/pycom_esp32/library/network.LoRa.html)

Produce a LoRa coverage map for your location of interest.