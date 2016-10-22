import sys
import time
from time import sleep
import os
 
print "::::::::::::::Program Starting::::::::::::::::::"

while 1:
    flag = "clear"
    try:
        read = open("test.txt", "r+")
        file = read.read()
        if(file != flag):
            sleep(.1)
            #file = read.read()
            read.close()
            if(len(file) == 0):
                pass
            else:
                print "Received signal:" + file
                write = open("test.txt", "w")
                write.write(flag)
                write.close()
    except(IOError):
        pass
    
