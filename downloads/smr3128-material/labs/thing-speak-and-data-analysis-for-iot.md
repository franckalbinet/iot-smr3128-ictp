ThingSpeak and Data analysis for IoT
==

我听见 我忘记; 我看见 我记住; 我做 我了解
*"I hear and I forget. I see and I remember. I do and I understand." --
 Confucius*


### Creating datastreams on Thingspeak

If we have an Internet connection, we can easily publish data from Raspberry Pi to Thingspeak, using MQTT. Here is an example:
http://community.thingspeak.com/tutorials/update-a-thingspeak-channel-using-mqtt-on-a-raspberry-pi/
In these original examples, data comes from the Raspi itself: CPU temperature, CPU load, memory usage. This might be used to monitor the status of computers in a school, public computers in a library etc.

Here we want to do IoT, so let us modify the original Python program, to take measurements from a TI Sensor Tag 
![](https://i.imgur.com/jn1yzcm.jpg)

http://processors.wiki.ti.com/index.php/SensorTag_User_Guide
connected by Bluetooth (BLE) to the Raspi.

We need the Bluez library for Raspberry Pi. 

An example of using it in Python to connect the Sensortag is found here:
https://smidgeonpigeon.wordpress.com/2015/07/21/raspberry-pi-2-ble-ti-sensor-tag/


### First example datastream: My Little Garden

I have now this system in my home, watching my little bamboo garden. 
![](https://i.imgur.com/hSOPcvn.jpg)

The Thingspeak channel is here:
https://thingspeak.com/channels/283445

The fields are:
1. Air humidity
2. Air temperature
3. Barometric pressure

The slightly modified Python source for streaming the TI Sensortag data is here:

```python
#!/usr/bin/env python
# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

from __future__ import print_function
import paho.mqtt.publish as publish
#import psutil
#import pyping
from bluepy import sensortag
from time import sleep

###   Start of user configuration   ###   

#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID
# Replace this with your Channel ID
channelID = "mygarden"
#channelID = "ping_rw"
#channelID = "cpu_usage"

# The Write API Key for the channel
# Replace this with your Write API key
apiKey = "OEF7BB0A58E69X1M"
#apiKey = "JZA2ZXCYYQU8CM4R"
#apiKey = "TZTN27QW1FADT9GZ"

#  MQTT Connection Methods

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
#useUnsecuredTCP = False
useUnsecuredTCP = True

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
#useSSLWebsockets = True
useSSLWebsockets = False

###   End of user configuration   ###

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
        
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey

# Connect to the TI sensortag
tag=sensortag.SensorTag("B4:99:4C:64:B4:21")
tag.IRtemperature.enable()
tag.humidity.enable()
tag.barometer.enable()
print ("Connected to sensortag")


# Run a loop which calculates the system performance every
#   20 seconds and published that to a ThingSpeak channel
#   using MQTT.
while(True):
    
    # get the system performance data
    #cpuPercent = psutil.cpu_percent(interval=20)
    #ramPercent = psutil.virtual_memory().percent
    #print (" CPU =",cpuPercent,"   RAM =",ramPercent)
    # get ping data
    #r = pyping.ping('tct.ac.rw')
    #pingLost = r.packet_lost
    #pingMin = r.min_rtt
    #pingMax = r.max_rtt
    refresh = True
    while refresh:
        try:
            baro = tag.barometer.read()
            humi = tag.humidity.read()
            temp = tag.IRtemperature.read()
            print (baro,humi,temp)
            refresh = False
        except:
           tag=sensortag.SensorTag("B4:99:4C:64:B4:21")
           tag.IRtemperature.enable()
           tag.humidity.enable()
           tag.barometer.enable()
           print ("Reconnected.")

    # build the payload string
    tPayload = "field1=" + str(humi[1]) + "&field2=" + str(temp[0]) + "&field3=" + str(baro[1])

    # attempt to publish this data to the topic 
    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")

    sleep(60)
```


The Sensor Tag has many more data sources, like accelerometer, magnetometer, radiative heat sensor etc.; but here we use only three of them.

We could analyze the data online, using the MATLAB services provided by Thingspeak. However, we will use an alternative method: we download the data and analyze it locally. 


### Second example: MQTT streaming from an ESP2866MOD node 

The ESP2866MOD is a low-cost WiFi-capable device, that can be programmed in Lua, or used as an Arduino. Here we connect a single moisture sensor to its analog port, and stream the data to Thingspeak, using the Arduino MQTT library. 

```C
#include "PubSubClient.h"
#include <ESP8266WiFi.h> //ESP8266WiFi.h
#include "credentials.h"  //This is a personal file containing web credentials

const char* ssid = WAN_SSID;
const char* password = WAN_PW;

//const char* topic = "channels/283445/publish/OEF7BB0A58E69X1M"; 
const char* topic = "channels/285666/publish/1YFS96FI67LX0AP6"; 
const char* server = "mqtt.thingspeak.com";

WiFiClient wifiClient;
PubSubClient client(server, 1883, wifiClient);

const int moisturePin = A0;
//const int temperaturePin = D0;

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
}


void setup() {
  Serial.begin(74880);
  delay(10);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

String clientName="ESP-Thingspeak";
  Serial.print("Connecting to ");
  Serial.print(server);
  Serial.print(" as ");
  Serial.println(clientName);
  
  if (client.connect((char*) clientName.c_str())) {
    Serial.println("Connected to MQTT broker");
    Serial.print("Topic is: ");
    Serial.println(topic);
    
    if (client.publish(topic, "hello from ESP8266")) {
      Serial.println("Publish ok");
    }
    else {
      Serial.println("Publish failed");
    }
  }
  else {
    Serial.println("MQTT connect failed");
    Serial.println("Will reset and try again...");
    abort();
  }
}

void loop() {
  static int counter = 0;
  int sensorValue = analogRead(moisturePin);
  String payload="field1=";
  payload+=sensorValue;
//  payload+="&field2=";
//  payload+=counter;
  payload+="&status=MQTTPUBLISH";
  
  if (client.connected()){
    Serial.print("Sending payload: ");
    Serial.println(payload);
    
    if (client.publish(topic, (char*) payload.c_str())) {
      Serial.println("Publish ok");
    }
    else {
      Serial.println("Publish failed");
    }
  }
  ++counter;
  delay(20000);
}

```
The data is collected at Thingspeak at my "soil" channel:
https://thingspeak.com/channels/285666



### Retrieving data from Thingspeak

We can download directly the accumulated data by navigating to "mygarden" -> "Data Import/Export" -> "Export" -> "Download". This will result in a CSV formatted spreadsheet, that is readable by e.g. LibreOffice.

Thingspeak also provides a Python interface for accessing uploaded data:
http://thingspeak.readthedocs.io/en/latest/index.html

We can use it either on the command line, or in a Python program. First, let's try to just get a CSV file from "My Little Garden".

```bash
thingspeak -q -r 100 -f csv 283445 > garden.csv
```

Unfortunately, the resulting file is not really a CSV file, only a printout of the data in Python format. Actually, CSV output is not yet implemented for the thingspeak Python module, only JSON; waiting for someone to do it <hint hint>!

On the other hand, working inside Python we can do better, creating any file formats, or processing the data directly. Getting the same data and then printing it out as a text file suitable for further processing is not much more difficult:

```Python
import thingspeak
import time
import sys

def main(count=8000):
  ch = thingspeak.Channel(283445)
  r=ch.get({'results': count})
  e=eval(r)
  f=e['feeds']
  x1=[eval(t['field1']) for t in f]
  x2=[eval(t['field2']) for t in f]
  x3=[eval(t['field3']) for t in f]
  tx=[time.mktime(time.strptime(t['created_at'],"%Y-%m-%dT%H:%M:%SZ")) for t in f]
  f=open("garden.dat","w")
  for i in range(len(x1)):
    f.write("%f %f %f %f\n" % (tx[i],x1[i],x2[i],x3[i]))
  f.close()

if __name__ == "__main__":
  main()
```
The generated datafile "garden.dat" is fine for plotting by Gnuplot, or for reading into Mathematica.

### Analyzing the data with Mathematica

It seems that having Mathematica for free on Raspi is somehow a well-kept secret. But it is there and it is great! 

If this is your first time with Mathematica, it will need some adjustments. We work with Notebooks, which are nicely formatted multimedia documents with executable content.

You can start Mathematica, and it will give you an empty Notebook. Type in your first instruction:

```Mathematica
x = Import["~/mqtt/garden.dat"];
Length[x]
```

When finished with the input, press <SHIFT> + <RETURN>. This will execute the code block under the cursor. A few other things useful to know:
* Put a semicolon ";" after the command to stop printing out the result
* Built-in functions and constants start with Capital letters, user stuff is supposed to be written with lowercase initials
* Function calls have the parameters in brackets: Sin[x]
* Lists are built with braces: {1, 2, 3, 5, 8}

If everything goes well, you should see the length of the imported data. 

Next, let us plot it:
```Mathematica
p = Transpose[x][[2]];
ListLinePlot[p]
```
The graph shows the 2nd data field, in our case the relative humidity. Easy, isn't it?

Now we are ready to do something more adventurous: let's try to predict the future! For this, we use the Mathematica function for generating a time series model.
```Mathematica
p1 = p[[1 ;; 600]];
tsm1 = TimeSeriesModelFit[p1];
ListLinePlot[{p1, TimeSeriesForecast[tsm1, {100}]}]
```
We have used only part of the recorded data for "learning" the model. We can compare the predicted and actual data; as we get more and more data, with more and more regularity (periodicity, trends), the prediction gets better and better.

