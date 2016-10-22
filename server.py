import serial
import datetime
import time
from time import sleep
import math
from time import clock
import sys
from socket import *

host = "127.0.0.1"
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print "waiting for messages..."

while True:
    try:
        (data, addr) = UDPSock.recvfrom(buf)
        print "Received messages: " + data
        if data:
            print "Velocity: " + data.split(",")[0]
            print "Distance: " + data.split(",")[1]
            print "data"
        if not data:
            print "empty"
    except KeyboardInterrupt:
        print '\nExiting gracefully...'
        UDPSock.close()
        break
sys.exit(0)
