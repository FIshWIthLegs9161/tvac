#!/usr/bin/env python3

import sys
import argparse
import serial
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from itertools import count
import pandas as pd
from matplotlib.animation import FuncAnimation
import threading
import time

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--baud", default="9600",
                help="baud rate of serial stream, defaults to 9600")
ap.add_argument("-p", "--port", default="/dev/ttyACM0",
                help="serial port, defaults to /dev/ttyACM0")
ap.add_argument("-o", "--output", default="output.csv",
                help="file name of the output file, defaults to output.csv")

args = vars(ap.parse_args())

print(args)
port = args["port"]
baud = args["baud"]

s = serial.Serial(port, baud)
writer = csv.writer(open(args["output"], "w"))
header = ["Time Stamp", "Δt", "yadda", "yadda2"]
writer.writerow(header)
t0 = datetime.now()

# Create figure for plotting
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 8
plt.rcParams["figure.figsize"] = fig_size
xs = [] #store trials here (n)
ys = [] #store relative frequency here
grn = [] #for theoretical probability
plt.style.use("fivethirtyeight")




def parse_serial_read(line):
    parse_list = []
    timestamp =  datetime.now().strftime("%c")
    parse_list.append(timestamp)

    #timedelta from start of data collection
    t = datetime.now() - t0
    t = int(t.total_seconds())
    parse_list.append(t)

    #parse the serial data
    #line = unicode(line, errors='ignore')
    line = line.decode("utf-8", errors='ignore')
    line_as_list=line.split('   ')

    parse_list = parse_list + line_as_list

    return parse_list

def plot_data(line):
    if len(line) is not 13:
        return

    xs.append(line[1]) #time on x-axis
    ys.append(float(line[3]))
    grn.append(float(line[4]))

    plt.subplots_adjust(left=0.35)
    plt.cla()
    plt.title('TVAC Data')
    plt.plot(xs, ys, "b", label="BLU", linewidth=1)
    plt.plot(xs, grn, "g", label="GRN", linewidth=1)
    plt.legend()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Temperature (°C)")

    set = "Set Point: " + line[7]
    error = "Error: " + line[8]

    plt.text(0.02, 0.45, set, fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.40, error, fontsize=14, transform=plt.gcf().transFigure)

    # write data to .csv file
    writer.writerow(line)
try:
    print ("Flushing Serial Data...")
    def animate(i):
        #get serial data and parse and plot
        if i>10:
            line = s.readline().strip()
            line = parse_serial_read(line)
            plot_data(line)
            print (line)
            print (i)

        #else:
            #sys.stdout.write('\r Waiting ')

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()


except KeyboardInterrupt:
    print("\nterminating...")
    #f.close()
    pass




































#l = l.decode("utf-8")
        #time = datetime.now()
        #time = time.strftime("%c")
        #print (time + "\t" + l)
        #f.writelines(time + "," + l + "\n")
