import serial
from time import sleep
import math
import re

# initialize serial port
ser1 = serial.Serial("/dev/ttyUSB0")
ser1.baudrate = 115200

print("Serial port configured.\n")
print("Beginning serial communication.\n")
ser1.flushInput()

VI = 0.0          #initial velocity, changes every iteration
VF = 0.0          #final velocity, changes every iteration
TS = 0.03        #time 
D = 0.0          #delta x

AX = 1.0;

#Build an averaging array (primitive LPF)
AMAG_ARRAY = [];
for i in range(0,50):
    AMAG_ARRAY.append(0)
AMAGF = 0.0

while True:

    
    # Send request to IMU for data
    ser1.write("accelp di.\r")

    # Wait for reponse
    sleep(TS)

    # Parse numbers from response
    imu_data = ser1.read(ser1.inWaiting()).strip()
    split_data = imu_data.split("\n")
    AX = float(split_data[1].split()[-1])
    AY = float(split_data[2].split()[-1])
    AZ = float(split_data[3].split()[-1])

    AX = AX * 9.810 / 1000                    #converts mill g to m/s^2
    AY = AY * 9.810 / 1000                    #converts mill g to m/s^2
    AZ = AZ * 9.810 / 1000                    #converts mill g to m/s^2
    if(pow(AX*AX+AY*AY+AZ*AZ,.5) > 9.9):
        VF = VI + AX * TS                        #v final  = v initial + accel * time sample
    else:
        VF = VI
        
    D = D + VF * TS
    VI = VF

    #Average values of the magnitude of [AX,AY,AZ] to get AMAGF
    AMAG_ARRAY.pop()
    AMAG_ARRAY.insert(0,pow(AX*AX+AY*AY+AZ*AZ,.5))
    AMAGF=0.0
    for g in AMAG_ARRAY:
        AMAGF=AMAGF+g/50

    #print(imu_data)
    #print(" ".join(match))
    #print(imu_data)
    #print(data)
    print("Distance: " + str(D))
    #print(VF)
    print("X Acceleration: " + str(AX))
    print("Y Acceleration: " + str(AY))   
    print("Z Acceleration: " + str(AZ))    
    print("Acceleration Magnitude: " + str(AMAGF))
    print("")

   

    
    










#comments: things to possibly remember
#port.flushInput()     
#print "Distance1 in cm: ", distance1
#print "The CHR value of rx: " + rx ,(i)
#print "The DEC value of rx:",ord(rx)
#print "The HEX value of rx:",hex(ord(rx))
#print "The BIN value of rx:",bin(ord(rx));
#print "\n"

    

 
