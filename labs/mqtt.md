# MQTT

> Building a MQTT broker using a RPi, sending data via WiFi, actuation using MQTT

Basically this lab is organized so that you can have an hands-on experience with MQTT and learn how to "publish" and "subscribe" to data. To this end you will use:
1. a "sandbox" broker
1. the ThingSpeak broker
1. your own broker

Among other things you will:
1. produce data using the command line
1. produce data by code using the LoPy devices
1. produce data to your own channel in ThingSpeak


## Hardware
Each group will use:
* A Raspberry Pi 3  with *Ubuntu MATE 16.04.2*
* A LoPy connected through a PySense board

The various elements are supposed to be connected as indicated in the figure below.
![The connections.](https://i.imgur.com/cYdNzFt.png)

For the next steps you will use one or more terminals (e.g., `xterm`)  connected to your Raspberry Pi via `ssh -X`.


## Installing the MQTT broker

There are various MQTT brokers that can be used with a Raspberry Pi device. A quite complete list can be found here https://github.com/mqtt/mqtt.github.io/wiki/servers

The most widely used are:
* http://mosquitto.org/
* http://www.hivemq.com/
* https://www.rabbitmq.com/mqtt.html
* http://activemq.apache.org/mqtt.html
* https://github.com/mcollina/mosca

For our experiments we will use [**Eclipse Mosquitto**](https://projects.eclipse.org/projects/technology.mosquitto). For more documentation check here: https://mosquitto.org/

### Installation steps:
To install the broker and some utilities you need to execute the following steps:

```shell=bash
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```


Once installed, please take a look at its [`man` page](https://mosquitto.org/man/mosquitto-8.html).

### Managing the broker

To check if the broker is running you can use the command:
```shell=bash
sudo netstat -tanlp | grep 1883
```
:::info
"tanlp" stands for: tcp, all, numeric, listening, program
:::
alternatively use:
```shell=bash
ps -ef | grep mosquitto
```

To start and stop its execution use:
```shell=bash
sudo /etc/init.d/mosquitto start/stop
```

if necessary, to avoid that it restarts automatically, do: `sudo stop mosquitto`

To run the broker execute:
```shell=bash
sudo mosquitto –v
```
:::info
"-v" stands for "verbose mode" and can be useful at the beginning to see what is going on in the broker. Can be convenient to use a dedicated terminal for the broker to execute in, if the "-v" option is used.
:::


## Clients for testing
The broker comes with a couple of useful commands to quickly publish and subscribe to some topic. Their basic syntax is the following. 
```shell
mosquitto_sub -h HOSTNAME -t TOPIC
mosquitto_pub -h HOSTNAME -t TOPIC -m MSG
```
More information can be found:
* https://mosquitto.org/man/mosquitto_sub-1.html
* https://mosquitto.org/man/mosquitto_pub-1.html

### First exercises:
Activate the broker with `mosquitto -v` in a terminal and open 2 more terminals, more or less like this:
![](https://i.imgur.com/KOcNjwz.jpg=400x400)
This way you'll control what your broker is doing.


Let's start with a easy one. In one terminal write:
```shell
mosquitto_sub -t i/LOVE/Python
```
the broker terminal should show something like:

![](https://i.imgur.com/5nMOywi.png)

the broker registered the subscription request of the new client. Now in another terminal, execute:
```shell
mosquitto_pub -t i/LOVE/Python -m "Very well!"
```
in the broker terminal, after the new registration messages, you'll also see something like:

![](https://i.imgur.com/s7zROiH.png)

meaning that the broker received the published message and that it forwarded it to the subscribed client. In the terminal where `mosquitto_sub` is executing you'll see the actual message appear.

:::warning
Try now `mosquitto_pub -t i/love/python -m "Also very well!"`. What happens? Are topics case-sensitive?
:::

Another useful option of `mosquitto_pub` is the following:
```shell 
mosquitto_pub -t i/LOVE/Python -l
```
it sends messages read from stdin, splitting separate lines into separate messages. Note that blank lines won't be sent. Give it a try.

Now let's experiment with *qos* and *retain*ed messages.

**qos (Quality of Service)**. Adding the `-q` option, for example to the `mosquitto_pub` you'll see the extra message that are now interchanged with the broker. For example, doing:
```shell
mosquitto_pub -t i/LOVE/Python -q 2 -m testing
```

you'll get:

![](https://i.imgur.com/wLqMrev.png)

compare this sequence of messages with the one obtanined with `-q 0` or with `-q 1`.

**Retained messages**. Normally if a publisher publishes a message to a topic, and *no one is subscribed* to that topic the message is simply discarded by the broker. If you want your broker to remeber the last published message you'll have to use the ```retain``` option. Only one message is retained per topic. The next message published on that topic replaces the retained message for that topic.
So try the following cases:
1. Retain message flag not set, like we did above, and check that the new subscriber doesn’t get the message i.e., no message is received.
1. Retain message flag set (`-r`) and the new subscriber gets the last message.
1. Retain message flag set and we publish several messages but the new subscriber only gets the last  message.

How do I remove or delete a retained message? You have to publish a blank message with the retain flag set to true which clears the retained message. Try it.


### Public brokers
There are also various public brokers in Internet, also called `sandboxes`. For example:
* `iot.eclipse.org`
    * more infos at: https://iot.eclipse.org/getting-started#sandboxes
* `test.mosquitto.org`
    * more infos at: http://test.mosquitto.org/
* `broker.hivemq.com`
    * more infos at: http://www.hivemq.com/try-out/
        * http://www.mqtt-dashboard.com/
        
we will always access them through the `1883`. Repeat the exercise above with one of these sandboxes (remember to use the `-h` option). Any difference?



## Accessing ThingSpeak via MQTT

ThingSpeak is an IoT analytics platform service that allows you to aggregate, visualize and analyze live data streams in the cloud. ThingSpeak provides instant visualizations of data posted by your devices to ThingSpeak. With the ability to execute MATLAB® code in ThingSpeak you can perform online analysis and processing of the data as it comes in. Some of the key capabilities of ThingSpeak include the ability to:

You will see much more about this platform in a later lab session.

### Creating a *channel*
You first have to sign in. Go to https://thingspeak.com/users/sign_up and create your own account. Then you can create your first channel. Like for example:
![](https://i.imgur.com/nN8iyWl.png)

In the "Private View" section you can get an overview of your data:
![](https://i.imgur.com/DzkbXVF.png)

Take a look to the other  sections. To connect to your channel you need the data in the API Keys section. In my case it says:
![](https://i.imgur.com/BlfIqlK.png)

Now, ThingSpeak offers either a REST and a MQTT API to work with channels. See here: https://es.mathworks.com/help/thingspeak/channels-and-charts-api.html
Unfortunately, for the moment, ThingSpeak supports only **publishing** to channels using MQTT.

### Exercise
Anyway, let's publish to a channel field feed using the infos that you can find here
https://es.mathworks.com/help/thingspeak/publishtoachannelfieldfeed.html and using `mosquitto_pub`.

![](https://i.imgur.com/f4vfCTZ.png)


# MQTT clients with MicroPython and the LoPy

## Installing the MQTT client library in the LoPy


The LoPy devices require a MQTT library to write the client application. The code can be found here: https://github.com/pycom/pycom-libraries/tree/master/lib/mqtt

You basically need to download the `mqtt.py` file and copy it in the `/flash/lib` directory of the device. 

## A simple subscriber

The code below represent a simple subscriber. As a first step it connects to the WiFi network available in the lab; you will have to properly configure the values to connect to your Wi-Fi access point.
In this case we will use the broker `test.mosquitto.org` but you can use the one on the Raspberry Pi.

```python=
from network import WLAN
from mqtt import MQTTClient
import machine
import time
import pycom

wifi_ssid = "LOCAL_AP"
wifi_passwd = ''
#broker_addr = "10.1.1.100"
broker_addr = "test.mosquitto.org"
MYDEVID = "PM"

def settimeout(duration):
   pass

def on_message(topic, msg):
    print("topic is: "+str(topic))
    print("msg is: "+str(msg))

### if __name__ == "__main__":

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == wifi_ssid:
        print('Network '+wifi_ssid+' found!')
        wlan.connect(net.ssid, auth=(net.sec, wifi_passwd), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print (wlan.ifconfig())
        break

client = MQTTClient(MYDEVID, broker_addr, 1883)
if not client.connect():
    print ("Connected to broker: "+broker_addr)

client.set_callback(on_message)
client.subscribe('lopy/sensor')

print('Waiting messages...')
while 1:
    client.wait_msg()

```

Now, in a terminal on your Raspberry Pi, type the command:
```shell=bash
mosquitto_pub -h test.mosquitto.org -t "lopy/sensor" -m "666"
```

What happens? Please, analyze the structure of the code. See the differences with the `Paho` code we saw in class? 

## A simple publisher

Let's produce some random data.  Copy the code below in your LoPy:

```python=
from network import WLAN
from mqtt import MQTTClient
import machine
import time
import pycom

import ucrypto
import math
import ujson

wifi_ssid = "LOCAL_AP"
wifi_passwd = ''
broker_addr = "10.1.1.100"
#broker_addr = "test.mosquitto.org"
MYDEVID = "PM"

def settimeout(duration):
   pass

def random_in_range(l=0,h=1000):
    r1 = ucrypto.getrandbits(32)
    r2 = ((r1[0]<<24)+(r1[1]<<16)+(r1[2]<<8)+r1[3])/4294967295.0
    return math.floor(r2*h+l)

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return random_in_range()

def on_message(topic, msg):
    # just in case
    print("topic is: "+str(topic))
    print("msg is: "+str(msg))

### if __name__ == "__main__":

pycom.heartbeat(False) # Disable the heartbeat LED

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == wifi_ssid:
        print('Network '+wifi_ssid+' found!')
        wlan.connect(net.ssid, auth=(net.sec, wifi_passwd), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print (wlan.ifconfig())
        break

client = MQTTClient(MYDEVID, broker_addr, 1883)
if not client.connect():
    print ("Connected to broker: "+broker_addr)

print('Sending messages...')
while True:
    # creating the data
    the_data = get_data_from_sensor()
    # publishing the data
    the_data_json = ujson.dumps(the_data)
    client.publish(MYDEVID+'/value', the_data_json)
    time.sleep(1)

```

Personalize the code with your own device id. Read the generated data using `mosquitto_sub`. We are using `ujson`, why?

---

# Final exercises
Now let's work on a couple of final exercises to mix up most of what we saw in this lab session.

## The first
Let's control the color of the LoPy's LED using MQTT.

![Test 1 scheme](https://i.imgur.com/y3gqrfN.png=400x400)

* Code “p1”: 
    * Have the LoPy receive "instructions" on the color that its LED has to show. The LoPy will be connected to its local broker in the Raspberry Pi.
	* To control the LED you can use the following code:
```python=
    if msg == b'GREEN':
        pycom.rgbled(0x007f00) # green
    elif msg == b'RED':
        pycom.rgbled(0xff0000) # red
    elif msg == b'OFF':
        pycom.rgbled(0x000000) # off
    else:
        pycom.rgbled(0x33ffff)
```
* Code “p2”:
	* You can use `mosquitto_pub`. Define the command required to change the color or turn off  the LED of the LoPy of a group next to you.



## The second
![Test 2 scheme](https://i.imgur.com/YHhxqVD.png=400x400)

For this exercise you have to use a unique   ("common") broker. It could either be one running in a Raspberry Pi in the lab or remote (e.g., test.mosquitto.org)

* Code “p1”: 
    * Reads the values of a specific sensor in the PySense and publish it periodically to the "common" broker
    * To get data from the PySense's sensors, you can extend the code of the function `get_data_from_sensor` we used before or, if the PySense is not available, use it as-is. 


```python=
def random_in_range(l=0,h=1000):
    r1 = ucrypto.getrandbits(32)
    r2 = ((r1[0]<<24)+(r1[1]<<16)+(r1[2]<<8)+r1[3])/4294967295.0
    return math.floor(r2*h+l)

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return random_in_range()
```

* Code “p2”:
    * Subscribe to all the values published in the "common" broker by the various groups in the lab, compute the average and visualize the value

Notes:
* please remind that code "p2" will use the Paho library version of MQTT, while the code "p1" will have to use the micropython version.
* you'll have to agree beforehand on the topic values

