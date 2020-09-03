#!/usr/bin/env python3

import argparse
import serial
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--baud", default="9600", help="baud rate of serial stream, defaults to 9600")
ap.add_argument("-p", "--port", default="/dev/ttyACM0", help="serial port, defaults to /dev/ttyACM0")
ap.add_argument("-o", "--output", default="output.csv", help="file name of the output file, defaults to output.csv")

args = vars(ap.parse_args())

print(args)
port = args["port"] 
baud = args["baud"] 

s = serial.Serial(port, baud)
f = open(args["output"], "w")
f.writelines("Time, Stat_0\n")
try:
    while True:
    
        l = s.readline().strip()
        l = l.decode("utf-8")
        time = datetime.now()
        time = time.strftime("%c")
        print (time + "\t" + l)
        f.writelines(time + "," + l + "\n")

except KeyboardInterrupt:
    print("\nterminating...")
    f.close()
    pass

