try:
  from usocket import socket
except:
  from socket import socket

import esp
esp.osdebug(None)

import gc
gc.collect()

import network
ap = metwork.WLAN(network.AP_IF)
ap.config(essid='brain', password='thisisaprototype')

if not ap.active():
  ap.active(True)