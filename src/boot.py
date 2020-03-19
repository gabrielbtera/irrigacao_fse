try:
  from usocket import socket, AF_INET, SOCK_STREAM
except:
  from socket import socket, AF_INET, SOCK_STREAM

import esp
esp.osdebug(None)

import gc
gc.collect()

import network
"""
ap = network.WLAN(network.AP_IF)

if not ap.active():
  ap.active(True)

ap.config(essid='brain', password='thisisaprototype')
print(ap.ifconfig())"""

ssid = ''
password = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
  pass

print("Connection successful!")
print(station.ifconfig())