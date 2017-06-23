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
import utils # utilities module with CRC calculation

# Initialize LoRa in LORA mode.
lora = LoRa(mode=LoRa.LORA)

# Get loramac as id to be sent in message
lora_mac = binascii.hexlify(network.LoRa().mac()).decode('utf8')

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

count_tx = 0

# tx loop
while True:
    s.setblocking(True)

    msgtx = str(count_tx) + ',' + lora_mac
    crc8 = utils.crc(msgtx.encode('utf8'))
    msgtx = msgtx + ',' + crc8

    s.send(msgtx)
    print('Tx: {} is sending data ...'.format(lora_mac))

    count_tx += 1

    # Get any data received...
    s.setblocking(False)
    data = s.recv(64)

    time.sleep(2)
