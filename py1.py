import sys
import time
from time import sleep

while 1:
    #response = raw_input("Enter data: ")
    read = open("test.txt", "r")
    file = read.read()
    if(file == "clear"):
        print "Received signal:" + file
        write = open("test.txt", "w")
        write.write("response")
        write.close()
    read.close()
                
