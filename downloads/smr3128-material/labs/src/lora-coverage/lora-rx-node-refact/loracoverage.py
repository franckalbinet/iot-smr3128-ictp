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
from machine import Timer
import json
import binascii
import sys
import _thread
import utils
import config

class LoraCoverage:

    def __init__(self, host, port, ssid, wpa, log_path):
        self.host = host
        self.port = port
        self.ssid = ssid
        self.wpa = wpa
        self.path = log_path

        self.gps_buffer = None
        self.log_time = None
        self.log_file = None
        self.rxnb = 0

        self.loramac = binascii.hexlify(network.LoRa().mac())

        # to be refactored
        self.end = False

        self.lock = _thread.allocate_lock()

        # Create proper directory for log file
        self._init_log()

        # Setup wypy/lopy as a station
        self.wlan = network.WLAN(mode=network.WLAN.STA)
        self.wlan.connect(self.ssid, auth=(network.WLAN.WPA2, self.wpa))

        while not self.wlan.isconnected():
            print('Connecting to Android WIFI HOTPOST...')
            time.sleep(1)

        print('Connected to Android WIFI HOTPOST')

        # Lora socket
        self.lora = None
        self.lora_sock = None

        # TCP socket
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect
        self.tcp_sock.connect((self.host, self.port))

    def _init_log(self):
        # create directory log if not exist
        try:
            os.mkdir(self.path)
        except OSError:
            pass

    # Check if string is empty
    def _isNotBlank (self, myString):
        return bool(myString and myString.strip())

    def _get_log_name(self):
        #print(self.log_time[:19])
        #print(type(ts))
        # ts = ts.replace('-', '')
        # ts = ts.replace('T', '')
        # ts = ts.replace(':', '')
        #ts = '1974'
        #base = self.path + '/acq/'
        #return base + ts + 'list.csv'
        return self.path + '/acq.list.csv'

    def _lora_cb(self, lora):
        events = lora.events()
        if (events & LoRa.RX_PACKET_EVENT) and (self.gps_buffer is not None):
            #if self.log_file is None:
            #    self.log_file = open(self._get_log_name(), 'w')

            data_rx = self.lora_sock.recv(256)
            stats = self.lora.stats()            # get lora stats (data is tuple)

            if self._isNotBlank(data_rx):
                with self.lock:
                    print(self.log_time)
                    print(self.gps_buffer)
                #print(self.gps_buffer['time'])
                # time_stamp = stats[0]          # get timestamp value
                # rssi = stats[1]
                # snr = stats[2]
                # sf = stats[3]
                #
                # msgData = ''
                # msgCrc = ''
                # if len(data_rx) >= 5:
                #     msg_data = data_rx[:-5]                  # remove the last 5 char data crc
                #     msg_crc = data_rx[-4:]                   # get the last 4 char
                #
                # # Calculate CRC
                # crc8 = utils.crc(msg_data)
                #
                # # Check CRC
                # crc_ok = True if crc8 == msg_crc.decode('utf-8') else False
                # # crc_ok = False
                # # if crc8 == msg_crc.decode('utf-8'):
                # #     crc_ok = True
                #
                # # fields_lorastats(LoraStats)
                #
                # # form csv row
                # msg = str(self.rxnb)
                # msg = msg + ',' + self.loramac.decode('utf8')
                # msg = msg + ',' + self.gps_buffer['time']
                # msg = msg + ',' + str(self.gps_buffer.lat)
                # msg = msg + ',' + str(self.gps_buffer.lon)
                # msg = msg + ',' + str(self.gps_buffer.alt)
                #
                # msg = msg + ',' + msg_data.decode('utf-8')
                # msg = msg + ',' + msg_crc.decode('utf-8')
                # msg = msg + ',' + str(crc8)
                # msg = msg + ',' + str(crc_ok)
                # msg = msg + ',' + str(time_stamp)
                # msg = msg + ',' + str(rssi)
                # msg = msg + ',' + str(snr)
                # msg = msg + ',' + str(sf)
                #
                # # # calc crc8 row
                # #crc8row = calc(msg.encode('utf-8'))
                # crc8row = utils.crc(msg.encode('utf-8'))
                #
                # # # add crc8row as last item
                # msg = msg + ',' + str(crc8row)
                #
                # # write csv and terminal
                # self.log_file.write(msg)
                # self.log_file.write('\n')
                # self.log_file.flush()
                #
                # print(msg)              # show in repl
                # self.rxnb += 1

    def start(self):
        # Initialize a LoRa sockect
        self.lora = LoRa(mode=LoRa.LORA)
        self.lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.lora_sock.setblocking(False)

        #self.tcp_alarm = Timer.Alarm(handler=lambda u: self._tcp_gps(), s=1, periodic=True)
        self.lora.callback(trigger=LoRa.RX_PACKET_EVENT, handler=self._lora_cb)

        # Start the TCP thread receiving GPS coordinates
        _thread.start_new_thread(self._tcp_thread, ())


    def stop(self):
        self.wlan.mode(network.WLAN.AP)
        self.tcp_sock.close()

        self.lora.callback(trigger=LoRa.RX_PACKET_EVENT, handler=None)
        self.lora_sock.close()
        #self.log_file.close()

        # Set end flag to terminate TCP thread
        self.end = True

    def _tcp_thread(self):
        while True:
            if self.end:
                _thread.exit()

            try:
                # Send request
                self.tcp_sock.send(b'?SHGPS.LOCATION;\r\n')
                # Get response
                rx_data = self.tcp_sock.recv(4096)

                # Release the lock in case of previous TCP error
                #self.lock.release()

                # Save last gps received to buffer
                with self.lock:
                    self.gps_buffer = json.loads(rx_data.decode('ascii'))
                    if not self.log_time:
                       self.log_time = self.gps_buffer['time']

            except socket.timeout:
                self.lock.locked()
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    pass
                else:
                    self.lock.locked()
                    print("Error: Android 'ShareGPS' connection status should be 'Listening'")
                    print('Change mode and soft reboot Pycom device')
            except Exception:
                self.lock.locked()
                print("TCP recv Exception")
            time.sleep(0.5)
