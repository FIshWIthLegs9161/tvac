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
import time

# Parse command line args
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--baud", default="9600",
                help="baud rate of serial stream, defaults to 9600")
ap.add_argument("-p", "--port", default="/dev/ttyACM0",
                help="serial port, defaults to /dev/ttyACM0")
ap.add_argument("-o", "--output", default="output.csv",
                help="file name of the output file, defaults to output.csv")
args = vars(ap.parse_args())
print(args)

# Setup Serial
port = args["port"]
baud = args["baud"]
ser = serial.Serial(port, baud)

# Setup output file
writer = csv.writer(open(args["output"], "w"))
header = ["Time Stamp", "deltaT", "t/4", "", "BLU", "GRN", "RED", "YELLOW", "SET", "Error"]
writer.writerow(header)

# Create figure for plotting data
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 8
plt.rcParams["figure.figsize"] = fig_size
plt.style.use("fivethirtyeight")

# Create lists for data
deltaT = [] #store trials here (n)
# Thermocouple lists
blu = [] #store relative frequency here
grn = [] #for theoretical probability
red = []
yel = []

# Index of the columns for each data type in the parsed serial read
deltaT_col = 1
blu_col = 4
grn_col = 5
red_col = 6
yel_col = 7
set_col = 8
err_col = 9

# Used to compute deltaT
t0 = datetime.now()

# Helper function to take the raw serial data and parse it to a list
def parse_serial_read(line):
    parse_list = []

    timestamp =  datetime.now().strftime("%c")
    parse_list.append(timestamp)

    # timedelta from start of data collection
    t = datetime.now() - t0
    t = int(t.total_seconds())
    parse_list.append(t)

    # parse the serial data
    line = line.decode("utf-8", errors='ignore')
    # currently delimited by '   ' but ideally could be \t for consistancy
    line_as_list=line.split('   ')

    parse_list = parse_list + line_as_list

    return parse_list

# Helper function to plot the parsed data into the figure and write to csv.
# Does some basic serial read error checking.
def plot_data(line):

    # sometimes the serial data comes in incomplete so this disgards those
    if len(line) is not 11:
        return
    # the first several serial reads can be 'corrupted' so discard the first 5
    if int(line[1]) < 5:
        return

    # add data points from line to each list
    deltaT.append(line[deltaT_col])
    blu.append(float(line[blu_col]))
    grn.append(float(line[grn_col]))
    red.append(float(line[red_col]))
    yel.append(float(line[err_col]))

    set = "Set Point: " + line[set_col]
    error = "Error: " + line[err_col]

    plt.subplots_adjust(left=0.35)
    plt.cla()
    plt.title('TVAC Data')

    plt.plot(deltaT, blu, "b", label="BLU", linewidth=1)
    plt.plot(deltaT, grn, "g", label="GRN", linewidth=1)
    plt.plot(deltaT, red, "r", label="RED", linewidth=1)
    plt.plot(deltaT, yel, "y", label="YELLOW", linewidth=1)

    plt.legend()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Temperature (°C)")

    plt.text(0.02, 0.45, set, fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.40, error, fontsize=14, transform=plt.gcf().transFigure)

    # write data to .csv file
    writer.writerow(line)

if __name__ == '__main__':
    try:
        print ("Flushing Serial Data...")
        def animate(i):
            #if i < 10:
            #    return
            #get serial data and parse and plot
            line = ser.readline().strip()
            line = parse_serial_read(line)
            plot_data(line)
            print (line)

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
