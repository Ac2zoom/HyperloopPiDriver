import serial
import time
from time import clock
from socket import *
import json
from queue import Queue
from threading import Thread

# Socket for communication with tac
host = "127.0.0.1"
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
# UDPSock.setblocking(0)

# Server Socket
# create an INET, STREAMing socket
server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host,
# and a well-known port
server_socket.bind((socket.gethostname(), 80))
# become a server socket
server_socket.listen(5)

print "waiting for messages..."

print "::::::::::::::Program Starting::::::::::::::::::"

# initialize serial ser #####################################
ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 9600
ser1 = serial.Serial("/dev/ttyUSB0")
ser1.baudrate = 115200

# global variables ###########################################
VI = 0.0        # initial velocity, changes every iteration
VF = 0.0        # final velocity, changes every iteration
TS = 0.05       # time
D = 0.0         # delta x
TF = 0.0        # ambient temp (Far....)
TC = 0.0        # ambient temp (Celcius)
ACT1 = 0        # actuator 1 position
ACT2 = 0        # actuator 2 position
ACT3 = 0        # actuator 3 position
DUTY = 0        # duty cycle of pwm

AX = 1.0;       # x acceleration
AY = 0          # y acceleration
AZ = 0          # z acceleration
GX = 0          # x angular velocity (gyro)
GY = 0          # y angular velocity (gyro)
GZ = 0          # z angular velocity (gryo)
pitch = 0       # Pitch
roll = 0        # Roll
yaw = 0         # Yaw
tempc = 0       # Temp ambient in pod (Celcius)
tempf = 0       # Temp ambient in pod (Far....)
distance1 = 0   # IR distance 1, Y position
distance2 = 0   # IR distance 2, Z position
tx = ""         # TX variable for sending commands
rx = ""         # RX variable for receiving commands

flag = "clear"
velocity = 0
distance = 0
THERMISTORC = 0
THERMISTORF = 0
IMURuntime = 0

# prints to let us know program is starting communication ######
print("Serial ser configured.\n")
print("Beginning serial communication.\n")

# flush both uart registers #####################################
ser.flushInput()
ser1.flushInput()

# Build an averaging array (primitive LPF) ######################
AMAG_ARRAY = [];
for i in range(0,50):
    AMAG_ARRAY.append(0)
AMAGF = 0.0


def sensor_comm():
    # main while loop, put code here ################################
    while True:

        start_time = time.time()

        # tx = raw_input("Enter command: ")
        data = ser.read(17).strip()
        if len(data) == 17:
            IR1 = ord(data[0]) * 256 + ord(data[1])
            global distance1
            if IR1 > 0:
                distance1 = pow((10 / (IR1 * .004888)), 1/0.9)

            IR2 = ord(data[2]) * 256 + ord(data[3])
            global distance2
            if IR2 > 0:
                distance2 = pow((10 / (IR2 * .004888)), 1/0.9)

            T0 = ord(data[4]) * 256 + ord(data[5])
            global TC
            global TF
            if T0 > 0:
                TC = (T0 * 500 / 1024) - 50
                TF = TC * 9/5 + 32

            global ACT1
            ACT1 = ord(data[6]) * 256 + ord(data[7])
            global ACT2
            ACT2 = ord(data[8]) * 256 + ord(data[9])
            global ACT3
            ACT3 = ord(data[10]) * 256 + ord(data[11])

            global DUTY
            DUTY = ord(data[12]) * 256 + ord(data[13])

            global THERMISTORC
            global THERMISTORF
            THERMISTORC = ord(data[14]) * 256 + ord(data[15])
            THERMISTORF = THERMISTORC * 9/5 + 32

        # ser.write(tx)

        # Send request to IMU for data
        ser1.write("accelp di. gyrop di. pitch di. roll di. yaw  di. temperature di.\r")

        # Wait for response
    #    sleep(TS)

        # Parse numbers from response
        imu_data = ser1.read(ser1.inWaiting()).strip()
        split_data = imu_data.split("\n")

        try:
            global AX
            AX = float(split_data[1].split()[-1])
            global AY
            AY = float(split_data[2].split()[-1])
            global AZ
            AZ = float(split_data[3].split()[-1])
            global GX
            GX = float(split_data[6].split()[-1])
            global GY
            GY = float(split_data[7].split()[-1])
            global GZ
            GZ = float(split_data[8].split()[-1])
            global pitch
            pitch = float(split_data[11].split()[-1])
            global roll
            roll = float(split_data[13].split()[-1])
            global yaw
            yaw = float(split_data[15].split()[-1])
            global tempc
            tempc = float(split_data[17].split()[-1])
            global tempf
            tempf = tempc * 9/5 + 32
            AX = AX * 9.810 / 1000                    # converts mill g to m/s^2
            AY = AY * 9.810 / 1000                    # converts mill g to m/s^2
            AZ = AZ * 9.810 / 1000                    # converts mill g to m/s^2
        except IndexError:
            print ""
        except ValueError:
            print ""

        # checks on the magnitude of the accelerations. Only calculates velocity
        # when our acceleration magnitude is greater than 9.8 m/s^2
        global VF
        global VI
        if pow(AX*AX+AY*AY+AZ*AZ,.5) > 9.9:
            VF = VI + AX * TS                        # v final  = v initial + accel * time sample
        else:
            VF = VI

        global D
        D += VF * TS  # distance = current distance + velocity * time
        VI = VF     # updates the current velocity

        # Average values of the magnitude of [AX,AY,AZ] to get AMAGF
        AMAG_ARRAY.pop()
        AMAG_ARRAY.insert(0, pow(AX*AX+AY*AY+AZ*AZ, .5))
        global AMAGF
        AMAGF = 0.0
        for g in AMAG_ARRAY:
            AMAGF += g / 50

        # time2 = clock()

        # if x acceleration goes over 2.0 g's, throw flag
        if AX > 9.6:
            ser.write('-')
        elif AX < -9.6:
            ser.write('+')
        elif distance > 1000:    # will change soonish to braking point
            if 130 < velocity < 150:
                ser.write('1')
            if 110 < velocity < 130:
                ser.write('2')
            if 90 < velocity < 110:
                ser.write('3')
            if 70 < velocity < 90:
                ser.write('4')
            if 50 < velocity < 70:
                ser.write('5')
            if 30 < velocity < 50:
                ser.write('6')
            if 10 < velocity < 30:
                ser.write('7')
            if 0 < velocity < 10:
                ser.write('8')

        # Test velocity
        global addr
        global velocity
        global distance
        try:
            (data, addr) = UDPSock.recvfrom(buf)
            if data:
                velocity = data.split(",")[0]
                distance = data.split(",")[1]
            if not data:
                pass
        except KeyboardInterrupt:
            print '\nExiting gracefully...'
            UDPSock.close()
            break

        # prints all incoming data from can system
        print "*************CAN DATA******************"
        print "IR Distance 1 in cm:   ", distance1
        print "IR Distance 2 in cm:   ", distance2
        print "Actuator 1:             %g" % ACT1
        print "Actuator 2:             %g" % ACT2
        print "Actuator 3:             %g" % ACT3
        print "Duty cycle:             %d" % DUTY
        print "Temperature in pod (C):", TC
        print "Temperature in pod (F):", TF
        print "Thermistor (C):         %d" % THERMISTORC
        print "Thermistor (F):         %d" % THERMISTORF
        print("\n")

        #prints all incoming data from IMU
        print "*************IMU DATA******************"
        print("X Gyro:                 " + str(GX))
        print("Y Gyro:                 " + str(GY))
        print("Z Gyro:                 " + str(GZ))
        print("X Acceleration:         " + str(AX))
        print("Y Acceleration:         " + str(AY))
        print("Z Acceleration:         " + str(AZ))
        print("Magnitude Acceleration: " + str(AMAGF))
        print("Pitch:                  " + str(pitch))
        print("Roll:                   " + str(roll))
        print("Yaw:                    " + str(yaw))
        print("IMU Temperature (F):    " + str(tempf))
        print("IMU Temperature (C):    " + str(tempc))
        print("Distance:               " + str(D))
        global IMURuntime
        IMURuntime = time.time() - start_time
        print "Runtime:               ", IMURuntime
        print("\n")

        # prints all incoming data from Hall Effect
        print "*************Hall DATA******************"
        print("Velocity (m/s):         " + str(velocity))
        print("Distance (m/s):        " + str(distance))
        print("\n")


def server():
    while 1:
        # accept connections from outside
        # Ensure that this connection is valid in test4
        (client_socket, address) = server_socket.accept()
        # now do something with the client_socket
        # in this case, we'll pretend this is a threaded server
        ct = Thread(target=client_thread, args=(client_socket,))
        ct.run()


def client_thread(client_socket):
    while True:
        data = {'IRDistance1': distance1, 'IRDistance2': distance2, 'Actuator1':
                ACT1, 'Actuator2': ACT2, 'Actuator3': ACT3, 'DutyCycle': DUTY,
                'TempInPodC': TC, 'TempInPodF': TF, 'ThermistorC': THERMISTORC,
                'ThermistorF': THERMISTORF, 'gyro': [GX, GY, GZ], 'acceleration':
                [AX, AY, AZ], 'pitch': pitch, 'roll': roll, 'yaw': yaw, 'IMUTempF':
                tempf, 'IMUTempC': tempc, 'IMUDistance': D, 'IMURuntime': IMURuntime,
                'velocity': velocity, 'HallDistance': distance}
        data['acceleration'].append(AMAGF)
        client_socket.send(json.dumps(data))

q = Queue()
commThread = Thread(target=sensor_comm, args=(q,))
serverThread = Thread(target=server, args=(q,))
commThread.start()
serverThread.start()
