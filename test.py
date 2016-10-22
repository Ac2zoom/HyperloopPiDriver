import serial
import time
import math

# initialize serial ser
ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 9600

print("Serial ser configured.\n")
print("Beginning serial communication.\n")

tx = "b"
rx = ""
distance1 = 0 
distance2 = 0
ser.flushInput()
while True:
    tx = raw_input("Enter command: ")        
    data = ser.read(6).strip()

    if(len(data) == 6):
        IR1 = ord(data[0]) * 256 + ord(data[1])
        if(IR1 > 0):
            distance1 = pow((10 / ( IR1 * .004888)),1/0.9)

        IR2 = ord(data[2]) * 256 + ord(data[3])
        if(IR2 > 0):
            distance2 = pow((10 / ( IR2 * .004888)),1/0.9)

        T0 = ord(data[4]) * 256 + ord(data[5])
        if(T0 > 0):
            TC = (T0 * 500 /1024) - 50
            TF =  TC * 9/5 + 32

        ser.write(tx)
    
    print "Distance1 in cm: ", distance1
    print "Distance2 in cm: ", distance2
    print "Temperature in pod (F):", TF 
    print "Temperature in pod (C):", TC
    print "\n"
    

 
