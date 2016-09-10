import serial
import time
import math

# initialize serial port
def setup():
    ser = serial.Serial("/dev/ttyS0")
    ser.baudrate = 9600

    print("Serial port configured.\n")
    print("Beginning serial communication.\n")
    return ser

def test(port):
    tx = ""
    rx = ""
    distance1 = 0 
    distance2 = 0
    i = 1
    port.flushInput()
    while True:
            
            first = port.read(1).strip()
            #port.flushInput()
            
            second = port.read(1).strip()
            #port.flushInput()
            
            third = port.read(1).strip()
            #port.flushInput()
            
            fourth = port.read(1).strip()
            #port.flushInput()

            temp0 = port.read(1).strip()
            #port.flushInput()
            
            temp1 = port.read(1).strip()
            #port.flushInput() 
            
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
                if total != 0:
                    distance2 = pow((10 / ( total2 * .004888)),1/0.9)

            if(len(temp0) != 0 and len(temp1) !=0):
                if ord(temp0) < 5:                          #put this in cause sometimes numbers will flip
                    total3 = ord(temp0) * 256 + ord(temp1)
                elif ord(temp0) > 5:
                    total3 = ord(temp1) * 256 + ord(temp0)

    
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

            port.flushInput() 
            #time.sleep(1)
            i = i + 1
    
def main():
    ser = setup()
    test(ser)

main()
 
