# --------------------------------------------------------
# read gps position using android smartphone
# data are saved in csv file
# see:
# https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/lora-mac.html
#
# android app ShareGPS:
# https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS
# http://www.jillybunch.com/sharegps/gpsd-commands.html
#
# caution:
# https://github.com/micropython/micropython/issues/2890
# OSError: [Errno 113] EHOSTUNREACH only when executing connect() in main.py
#
# caution:
# to use two sockets together (wifi and lora):
# 1) open socket1
# 2) work with socket1
# 3) close socket1
# 4) open socket2
# 5) work with socket2
# 6) close socket2
# 7) insert a delay (actually 0.3 sec, time.sleep(0.3))
#
# other info about sockets
# http://stackoverflow.com/questions/1908878/netcat-implementation-in-python
# https://gist.github.com/adventureloop/9bba49b214768ed36717060246d18916


import os
import pycom
import network
import time
import socket
from machine import Pin
from machine import SD
import binascii
from network import LoRa
import machine
import json
import binascii
import sys
import utils

# gps data
lat = 0.0
lon = 0.0
alt = 0.0
gpstime = ""

# rssi data
timestamp = ""
rssi = ""
snr = ""
sf = ""

# use tcp to send gps request position.
# It is equivalent to:
# netcat(192.168.43.1, 2947, '?SHGPS.LOCATION;')
#
def GetGpsPosition(host, port):
    global lat
    global lon
    global alt
    global gpstime

    data = b'?SHGPS.LOCATION;\r\n'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # get data after connection
    rxdata = sock.recv(4096)
    sock.send(data)
    # get answer
    rxdata = sock.recv(4096)
    jsrx = rxdata.decode('ascii')

    #jsrx = repr(rxdata)
    # http://stackoverflow.com/questions/4987327/how-do-i-check-if-a-string-is-unicode-or-ascii
    # convert bytes (python 3) or unicode (python 2) to str
    # if str(type(jsrx)) == "<class 'bytes'>":
    #     # only possible in Python 3
    #     jsrx = jsrx.decode('ascii')  # or  s = str(s)[2:-1]
    # elif str(type(jsrx)) == "<type 'unicode'>":
    #     # only possible in Python 2
    #     jsrx = str(jsrx)



    # ------------------- parse json string
    # see:
    # http://stackoverflow.com/questions/7771011/parse-json-in-python
    # http://stackoverflow.com/questions/15010418/parsing-json-array-in-python
    #
    # now jsrx has the json string
    # example of string received from android app:
    # {'lat': 45.70373, 'time': '2017-04-24T12:35:20.000Z', 'alt': 57.45, 'class': 'SHGPS.LOCATION', 'lon': 13.72005, 'mode': 2}
    #
    json_data = json.loads(jsrx)
    lat = json_data["lat"]
    lon = json_data["lon"]
    alt = json_data["alt"]
    gpstime = json_data["time"]

    sock.close()

# check if string is empty
def isNotBlank (myString):
    return bool(myString and myString.strip())


# ================================================
# Start program
#
# get the 6-byte unique id of the board (pycom MAC address)
# get loramac

loramac = binascii.hexlify(network.LoRa().mac())

# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA)

# create a raw LoRa socket
nMsgTx = 1
tStartMsec = time.ticks_ms()
LoraStats = ""                          # get lora stats

# ----------------------------- tstgps5.py
# expansion board user led
user_led = Pin("G16", mode=Pin.OUT)
# expansion board button
button = Pin("G17", mode=Pin.IN, pull=Pin.PULL_UP)

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # green

# ---------------------------------
# setup wypy/lopy as a station
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect('mrandroid', auth=(network.WLAN.WPA2, 'eatmenow'))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())

# ---------------------------------
# create directory log if not exist
try:
    os.mkdir('/flash/log')
except OSError:
    pass

# open file to store csv
# form name of csv file
# format: acq<year><month><day><hour><min><sec>

# unpack localtime in year...
year, month, day, hour, minute, second, ms, dayinyear = time.localtime()

nameCsv = '/flash/log/acq'
nameCsv = nameCsv + '{:04d}'.format(year)
nameCsv = nameCsv + '{:02d}'.format(month)
nameCsv = nameCsv + '{:02d}'.format(day)
nameCsv = nameCsv + '{:02d}'.format(hour)
nameCsv = nameCsv + '{:02d}'.format(minute)
nameCsv = nameCsv + '{:02d}'.format(second)
nameCsv = nameCsv + 'list.csv'

fCsv = open(nameCsv, 'w')

# ---------------------------------
pressed = 0
count = 0
while True:
    GetGpsPosition("192.168.43.1", 2947)

    # create a raw LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    s.setblocking(False)
    # dataRx = s.recv(64)
    dataRx = s.recv(256)
    LoraStats = lora.stats()            # get lora stats (data is tuple)

    if isNotBlank (dataRx):
        timestamp=LoraStats[0]          # get timestamp value
        rssi=LoraStats[1]
        snr=LoraStats[2]
        sf=LoraStats[3]

        msgData=""
        msgCrc=""
        if len(dataRx)>=5:
            msgData = dataRx[:-5]                  # remove the last 5 char data crc
            msgCrc = dataRx[-4:]                   # get the last 4 char

        # calc crc
        crc8 = utils.crc(msgData)
        # verify crc
        crcOk = False
        if crc8 == msgCrc.decode('utf-8'):
            crcOk = True

        # fields_lorastats(LoraStats)

        # form csv row
        msg = str(count)
        msg = msg + ',' + loramac.decode('utf8')
        msg = msg + ',' + gpstime
        msg = msg + ',' + str(lat)
        msg = msg + ',' + str(lon)
        msg = msg + ',' + str(alt)

        msg = msg + ',' + msgData.decode('utf-8')
        msg = msg + ',' + msgCrc.decode('utf-8')
        msg = msg + ',' + str(crc8)
        msg = msg + ',' + str(crcOk)
        msg = msg + ',' + str(timestamp)
        msg = msg + ',' + str(rssi)
        msg = msg + ',' + str(snr)
        msg = msg + ',' + str(sf)

        # # calc crc8 row
        #crc8row = calc(msg.encode('utf-8'))
        crc8row = utils.crc(msg.encode('utf-8'))

        # # add crc8row as last item
        msg = msg + ',' + str(crc8row)

        # write csv and terminal
        fCsv.write(msg)
        fCsv.write('\n')
        fCsv.flush()

        print(msg)              # show in repl

        count = count + 1

    s.close()
    time.sleep(0.3)  #<== Try a delay here...

    if button() == 0:
        print("Acquisition ended")
        wlan.mode(network.WLAN.AP)
        pycom.rgbled(0x7f0000) # red
        break
