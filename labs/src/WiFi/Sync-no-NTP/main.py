import machine
from network import WLAN
import time
import socket
import utime

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'FabLab':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'MakerFaire'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

rtc = machine.RTC()
rtc.init((2015, 1, 1, 1, 0, 0, 0, 0))
print("Before network time adjust", rtc.now())
print('Setting RTC using Sodaq time server')

s=socket.socket()
addr = socket.getaddrinfo('time.sodaq.net', 80)[0][-1]
s.connect(addr)
s.send(b'GET / HTTP/1.1\r\nHost: time.sodaq.net\r\n\r\n')
ris=s.recv(1024).decode()
s.close()
rows = ris.split('\r\n')            # transform string in list of strings
seconds = rows[7]
print (seconds)
print("After network time adjust")
rtc.init(utime.localtime(int(seconds)))
print(rtc.now())
