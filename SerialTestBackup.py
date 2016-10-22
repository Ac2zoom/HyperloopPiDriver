import serial
import time
import math

# initialize serial ser
ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 9600

print("Serial ser configured.\n")
print("Beginning serial communication.\n")

tx = "test"
rx = ""
distance1 = 0 
distance2 = 0
ser.flushInput()
while True:
            
    first = ser.read(1).strip()
    second = ser.read(1).strip()
    third = ser.read(1).strip()            
    fourth = ser.read(1).strip()
    temp0 = ser.read(1).strip()            
    temp1 = ser.read(1).strip()
            
    if(len(first) != 0 and len(second) !=0):
        if ord(first) < 5:                          #put this in cause sometimes numbers will flip
            total = ord(first) * 256 + ord(second)
        else:
            total = ord(second) * 256 + ord(first)
    if total != 0:
        distance1 = pow((10 / ( total * .004888)),1/0.9)

    if(len(third) != 0 and len(fourth) !=0):
        if ord(third) < 5:                          #put this in cause sometimes numbers will flip
            total2 = ord(third) * 256 + ord(fourth)
        elif ord(third) > 5:
            total2 = ord(fourth) * 256 + ord(third)
        if total2 != 0:
            distance2 = pow((10 / ( total2 * .004888)),1/0.9)

    if(len(temp0) != 0 and len(temp1) !=0):
        if ord(temp0) < 5:                          #put this in cause sometimes numbers will flip
            total3 = ord(temp0) * 256 + ord(temp1)
        elif ord(temp0) > 5:
            total3 = ord(temp1) * 256 + ord(temp0)

    ## write data to serial ser
    ## test string is "test"
    ser.write(tx)

    
    #print "Sensor1 voltage(digital):", total
    print "Distance1 in cm: ", distance1
    print "Distance2 in cm: ", distance2
    print "Temperature in room (F):", ((total3 * 500 /1024) - 50) * 9/5 + 32  
    print "Temperature in room (c):", ((total3 * 500 /1024) - 50)
    print "\n"
              


            #print "The CHR value of rx: " + rx ,(i)
            #print "The DEC value of rx:",ord(rx)
            #print "The HEX value of rx:",hex(ord(rx))
            #print "The BIN value of rx:",bin(ord(rx));
            #print "\n"

    ser.flushInput() 
    

 
