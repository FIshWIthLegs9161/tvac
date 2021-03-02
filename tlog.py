#!/usr/bin/e nv python3

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
header = ["Time Stamp", "deltaT", "t/4", "TC1", "TC2", "TC3", "TC4", "TC5", "TC6",
          "TC7", "TC8", "SET", "Error", "Int", "Der", "Ontime"]
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

tc1 = []
tc2 = []
tc3 = []
tc4 = []
tc5 = []
tc6 = []
tc7 = []
tc8 = []

# Index of the columns for each data type in the parsed serial read
deltaT_col = 1

tc1_col = 3
tc2_col = 4
tc3_col = 5
tc4_col = 6

tc5_col = 10 #7
tc6_col = 9 #8
tc7_col = 8 #9
tc8_col = 7 #10

#blu_col = 4
#grn_col = 5
#red_col = 6
#yel_col = 7
set_col = 11
err_col = 12

# Used to compute deltaT
t0 = datetime.now()

# Helper function to take the raw serial data and parse it to a list
def parse_serial_read(line):
    parse_list = []

    timestamp = datetime.now().strftime("%c")
    parse_list.append(timestamp)

    # timedelta from start of data collection
    t = datetime.now() - t0
    t = int(t.total_seconds())
    parse_list.append(t)

    # parse the serial data
    line = line.decode("utf-8", errors='ignore')
    # delimited by \t 
    line_as_list=line.split('\t')

    parse_list = parse_list + line_as_list
    
    
    return parse_list

# Helper function to check for valid serial read
def validate_parse(line):

    if len(line) is not 16:
        return False

    # check last 13 elements for vaild float values, discard if not valid
    valid_line = line[-13:]
    for i in range(len(valid_line)):
        try:
            valid_line[i] = float(valid_line[i])
        # print error and failed parse to console for troubleshooting
        except Exception as ex:
            print ("************* Parse failed: ********************")
        
            for x in header[1:]:
                print(x, end ="\t")
            print()
            for x in line[1:]:
                print(x, end="\t")
            print()
            print()
            
            return False

    # join list with time stamp
    valid_line = line[:3] + valid_line


    print ("Parse success:")
        
    for x in header[1:]:
        print(x, end ="\t")
    print()
    for x in valid_line[1:]:
        print(x, end="\t")
    print()
   
    
    # write line to csv file
    writer.writerow(valid_line)
    return (valid_line)
  

# Helper function to plot the parsed data into the figure and write to csv.
def plot_data(line):
    
    set = "Set Point: " + str(line[set_col])
    error = "Error: " + str(line[err_col])

    plt.subplots_adjust(left=0.35)
    plt.cla()
    plt.title('TVAC Data')


    # add data points from line to each list
    '''
    try:
        deltaT.append(line[deltaT_col])
        #plt.plot(deltaT, tc1, label="tc1", linewidth=1)
    except Exception as e:
        print(e)
    '''
    #print(line)
    try:
        #print(float(line[tc1_col]))
        deltaT.append(line[deltaT_col])
        tc1.append(line[tc1_col])
        tc2.append(line[tc2_col])
        tc3.append(line[tc3_col])
        tc4.append(line[tc4_col])
        tc5.append(line[tc5_col])
        tc6.append(line[tc6_col])
        tc7.append(line[tc7_col])
        tc8.append(line[tc8_col])

    except Exception as e:
        print ("tc1 error: ")
        print(e)

    '''
    try:
        tc2.append(float(line[tc2_col]))
        plt.plot(deltaT, tc2, label="tc2", linewidth=1)
    except Exception as e:
        print ("tc2 error: ")
        print(e)
    try:
        t
        plt.plot(deltaT, tc3, label="tc3", linewidth=1)
    except Exception as e:
        print ("tc3 error: ")
        print(e)
    try:
        
        plt.plot(deltaT, tc4, label="tc4", linewidth=1)
    except Exception as e:
        print ("tc4 error: ")
        print(e)
    try:
        
        plt.plot(deltaT, tc5, label="tc5", linewidth=1)
    except Exception as e:
        print ("tc5 error: ")
        print(e)
    try:
        
        plt.plot(deltaT, tc6, label="tc6", linewidth=1)
    except Exception as e:
        print ("tc6 error: ")
        print(e)
    try:
        
        plt.plot(deltaT, tc7, label="tc7", linewidth=1)
    except Exception as e:
        print ("tc7 error: ")
        print(e)
    try:
        
        plt.plot(deltaT, tc8, label="tc8", linewidth=1)
    except Exception as e:
        print ("tc8 error: ")
        print(e)
    '''

        
        


    
    
    plt.plot(deltaT, tc1, "b", label="tc1", linewidth=1)
    plt.plot(deltaT, tc2, "g", label="tc2", linewidth=1)
    plt.plot(deltaT, tc3, "r", label="tc3", linewidth=1)
    plt.plot(deltaT, tc4, "y", label="tc4", linewidth=1)
    plt.plot(deltaT, tc5, "b", label="tc5", linewidth=1)
    plt.plot(deltaT, tc6, "g", label="tc6", linewidth=1)
    plt.plot(deltaT, tc7, "r", label="tc7", linewidth=1)
    plt.plot(deltaT, tc8, "y", label="tc8", linewidth=1)
    
    
    plt.legend()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Temperature (°C)")
    
    plt.text(0.02, 0.45, set, fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.40, error, fontsize=14, transform=plt.gcf().transFigure)
    
    
    # write data to .csv file
    #writer.writerow(line)

if __name__ == '__main__':
    try:
        print ("Flushing Serial Data...")
        while 1:
            def animate(i):
                #if i < 10:
                #    return
                #get serial data and parse and plot
                line = ser.readline().strip()
                line = parse_serial_read(line)
                line = validate_parse(line)
                if line:
                    print()
                    plot_data(line)
                
                #print (line)
                #print(tc1) 
            def animate(i):

            ani = FuncAnimation(plt.gcf(), animate, interval=1000)
            plt.tight_layout()
            plt.show()


    except KeyboardInterrupt:
        print("\nterminating...")
        #f.close()
        pass
