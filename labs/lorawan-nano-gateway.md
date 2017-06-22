**LoRaWAN**: connect a LoPy to a LoRaWAN network such as The Things Network (TTN)

# LoRaWAN Nano-Gateway

## Introduction
In this example, we wan to route data sent from a Lopy node to a LoRaWAN network (TTN). Data that can be further used in various applications. We will hence set up:
* a TTN LoRaWAN network (Gateway, application and devices)
* a Lopy node (with OTAA authentication activated) sending data (LoRa)
* a Lopy node acting as a Gateway forwarding packets to TTN.

## Learning outcomes

You will learn how to:
* register a device, gateway and application to a LoRaWAN network such as The Things Network (TTN);
* set up a Lopy as a Nano-Gateway;
* and send data over the network from a Lopy node.

## Required Components

For this example you will need:

- a LoPy or WiPy module that will be used as a Gateway
- a LoPy or WiPy module that will be used as a Node
- two microUSB cables
- a development PC
- a TTN account

The source code is in the `src/lorawan-nano-gateway` directory.

> Always update the firmware to the most recent version.

## 1. Gateway setup

First create an account https://www.thethingsnetwork.org/

Once logged in, open TTN console:

![img/ttn-log-console.png](http://i.imgur.com/aG3umEu.png)


### 1.1 Configure a Gateway in TTN

Click on `Gateways` box

![img/app-or-gw.png)](http://i.imgur.com/TYb1HbI.png)


Click on `register gateway` link or `Get started by registering one`

![img/register-gw-link.png](http://i.imgur.com/ozGNHW4.png)


Reproduce the settings below, with: 
* `I'am using the legacy packet forwarder` checkbox checked
* **Gateway EUI**: an 8-bytes valid hexadecimal ID of your choice but if you take a look at the first 2 lines in `src/lorawan-nano-gateway/gateway/config.py`:

```python
import machine
import binascii

WIFI_MAC = binascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]
```

the Gateway ID will be generated automatically using your node's unique ID. So connect to the Lopy your are going to use as Gateway and run these 4 lines of code, `print(GATEWAY_ID)` and that's the hexadecimal ID you will use to fill the **Gateway EUI** input box.

* **Description**: A name of your choice
* **Frequency plan**: Choose based on gateway's location

![img/frequency-plan.png](http://i.imgur.com/Wkg3jZ3.png)

* **Router**: Choose based on gateway's location

![img/router.png](http://i.imgur.com/90u3bB6.png)
 
![img/register-gw.png](http://i.imgur.com/WoqVGMU.png)

* Locate your gateway on a map (click on location to move the marker). This will be used as Metadata.

* Finally, specify Gateway's Antenna placement and `Register`

![img/antenna-register](http://i.imgur.com/ezqRr7S.png)


### 1.2 Set up a Lopy as a Nano-Gateway

Now we have configured a Gateway in TTN LoRaWAN network, we need to set up a node (a physical device) operating as a Gateway.

To do so:

* edit the configuration file`src/lorawan-nano-gateway/gateway/config.py` (see file below) to specify your WIFI SSID and KEY;
* connect to the Lopy of your choice (the one acting as gateway);
* and sync the `src/lorawan-nano-gateway/gateway/` folder content to your Lopy.


`src/lorawan-nano-gateway/gateway/config.py`:

```python
""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import binascii

WIFI_MAC = binascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
GATEWAY_ID = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]

SERVER = 'router.eu.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'your-wifi-ssid'
WIFI_PASS = 'your-wiki-key'

LORA_FREQUENCY = 868100000
LORA_DR = "SF7BW125" # DR_5
```

* reboot your Lopy and after few seconds, minutes, you should be able to see your Gateway with status `connected`:

![img/gw-connected.png](http://i.imgur.com/S5IJSTY.png)


## 2. Node/device setup
By now, you should have a running and connected gateway. We will now set up both TTN and the Lopy node to get access to node's data in the LoRaWAN network.

### 2.1 Create a TTN application

First go to the **TTN console** and create a new application:

![img/ttn-app-link.png](http://i.imgur.com/WxuPy0G.png)

Then fill the following form as below:
* **Application ID**: any unique identifier of your choice
* **Description**: a free description of your app.

and click `Add application` button (on the bottom right).

![img/my-demo-app.png](http://i.imgur.com/8fnJAad.png)

You should now end up with a fresh new application:

![img/fresh-new-app.png](http://i.imgur.com/qaIzJ4H.png)

### 2.2 Register a new device

To register a new device (our Lopy node), click on `Devices` button (top right), `register a new device` and fill the form accordingly:

* **DeviceID**: unique ID of your choice
* **DeviceEUI**: click on highlighted button to toggle the auto-generated mode
* **AppKey**: idem

and finally click on `Register`.

![device-form.png](http://i.imgur.com/yehgBmX.png)


Generated **DeviceEUI, AppEUI** and **AppKey** (the latter has been generated when we created the app.) will be used to configure our Lopy node.

![my-demo-device.png](http://i.imgur.com/thbZ4lU.png)

Notice that device's `Status` is `never seen`for now. The last step is now to set up our Lopy node.

### 2.3 Set up an authenticated (OTAA) Lopy node

You will find the required files under `src/lorawan-nano-gateway/node` directory.

In `src/lorawan-nano-gateway/node/main.py` file 

```python
dev_eui = binascii.unhexlify('your-dev-id'.replace(' ',''))
app_eui = binascii.unhexlify('your-app-id'.replace(' ',''))
app_key = binascii.unhexlify('your-app-key'.replace(' ',''))
```

Replace, `'your-dev-id'`, `'your-app-id'` and `'your-app-key'` as configured in TTN.

Sync. the entire `/src/lorawan-nano-gateway/node` folder to the Lopy acting as node and reboot your node.

## 3. Checking that our LoRaWAN network is up and running

If the process has been correctly completed, in the TTN console under:

APPLICATIONS &#9654; `"your-application-name"` &#9654; DEVICES &#9654; `"your-device-name"` &#9654; DATA

you should be able to see data sent from your Lopy node in TTN itself:

![img/data-received-ttn.png](http://i.imgur.com/pB1iOwQ.png)


If you click on the up arrow of one of the message, you will open a panel with details of the **Payload** (data itself) with associated metadata:

![img/data-received-ttn-unfold](http://i.imgur.com/I50DMk8.png)



## Exercises

### Tip 1

The payload received from your device often need to be decoded (from bytes to whatever you want)

![img/ttn-payload.png](http://i.imgur.com/LUNPjJL.png)

the JavaScript snippet code gives a decoding example:

```javascript
function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  len = bytes.length
  
  decoded = bytes.map(function(d) { return String.fromCharCode(d); })
  decoded[len - 1] = bytes[len - 1]
  return {'data': decoded.join('')}
}
```

### Tip 2

This is obviously possible to retrieve data sent from your device directly from a Jupyter notebook. The Python snippet code below gives an example.

Copy the following Python snippet code in a Jupyter notebook (with Python kernel 2.7):

```python
import pandas as pd
import requests

url_data_dev = 'https://my-demo-application.data.thethingsnetwork.org/api/v2/query/my-demo-device'

headers = {'Authorization': 'your key'}

# Packages the request, send the request and catch the response: r
r = requests.get(url_data_dev, headers=headers)

# Extract the response: text
text = r.text

df = pd.read_json(text)
df = df.set_index(['time'])
df.head()
```

### Challenge

Measure the temperature with a Pysense and retrieve it from TTN or even better from a Jupyter notebook in a tabular form and time line chart.
