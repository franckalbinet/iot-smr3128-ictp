# ---------------------------------------------------
# tx messages with lora-mac
# see:
# loramac
# https://docs.pycom.io/pycom_esp32/pycom_esp32/tutorial/includes/lora-mac.html
# https://forum.pycom.io/topic/934/lora-stats-documentation-is-missing-the-parameter-must-passed/2

import network
from network import LoRa
import binascii
import socket
import machine
import time
import binascii
import sys

# crc calc
#
def calc(incoming):
    # convert to bytearray
    hex_data = incoming.decode("hex")
    msg = bytearray(hex_data)
    check = 0
    for i in msg:
        check = AddToCRC(i, check)
    return hex(check)

def AddToCRC(b, crc):
    if (b < 0):
        b += 256
    for i in range(8):
        odd = ((b^crc) & 1) == 1
        crc >>= 1
        b >>= 1
        if (odd):
            crc ^= 0x8C # this means crc ^= 140
    return crc

# --------------------------------------------
# start:
#
# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA)

# get loramac
loramac = binascii.hexlify(network.LoRa().mac())
# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
countTx = 0

# tx loop
while True:
    # send data
    s.setblocking(True)
    # calc crc
    msgtx = str(countTx) + ',' + loramac.decode('utf8')
    crc8 = calc(msgtx.encode('utf8'))
    msgtx = msgtx + ',' + crc8

    s.send(msgtx)
    countTx = countTx + 1

    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    # time.sleep(machine.rng() & 0x0F)
    time.sleep(2)               # sleep 2sec
