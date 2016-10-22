import serial
import datetime
import time
from time import sleep
import math
from time import clock
import RPi.GPIO as GPIO
import os
from socket import *

host = "127.0.0.1"
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
           
radius = 0.0762 * 5 # meters (3 inches)
circumference = 2 * math.pi * radius 
speed_1 = 0
speed_2 = 0 
dt_1 = 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
dt_2 = 0
dt_total = 0
distance_1 = 0
distance_2 = 0
start_time_1 = 0
start_time_2 = 0
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, 0)           #0 output
GPIO.setup(13, 1)           #1 input
GPIO.setup(5, 1)

print "::::::::::::::Program Starting::::::::::::::::::"
while 1:
    
    start = time.time()
    if GPIO.input(13) == 1:
        dt_1 = time.time() - start_time_1
        rpm = 60 / dt_1
        #print "rpm: " + str(rpm)
        speed_1 = circumference / dt_1
        distance_1 += circumference
        #print "1: " + str(speed_1)
        #print "1: " + str(distance_1)
        start_time_1 = time.time()
        while GPIO.input(13) == 0:
            pass

        
# @TODO Make sure that this statement does not block reading from the other sensor.            
       
    if GPIO.input(5) == 1:
        dt_2 = time.time() - start_time_2
        speed_2 = circumference / dt_2
        distance_2 += circumference
        #print "2: " + str(speed_2)
        #print "2: " + str(distance_2)
        start_time_2 = time.time()
        while GPIO.input(5) == 0:
            pass
        #print "latency: " + str(time.time() - start)

    #need count because if not, socket buffer fills way to fast and client slowly picks data from front of buffer
    if(count == 100000):
        velocity = max([speed_1,speed_2])
        distance = max([distance_1,distance_2])
        print "max velocity =========> : " + str(velocity)
        print "max distance =========> : " + str(distance)
        data = str(velocity) + ", " + str(distance)
        UDPSock.sendto(data, addr)
        if data == "exit":
            break
        count = 0
    else:
        count = count + 1
   
           
