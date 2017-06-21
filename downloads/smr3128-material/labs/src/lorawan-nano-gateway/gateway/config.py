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

WIFI_SSID = 'Bbox-E8920087'
WIFI_PASS = '55FE992DEC17963FCFAF2A461ED53E'

LORA_FREQUENCY = 868100000
LORA_DR = "SF7BW125" # DR_5
