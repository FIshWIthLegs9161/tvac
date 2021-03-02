#!/usr/bin/python

import serial,time,copy, argparse

# Parse user arguments:
parser = argparse.ArgumentParser()
parser.add_argument("Filename", help="Log-Filename.csv. The name of the file.", type=str)
parser.add_argument("Frequency", help="Time interval between samples in seconds.",type=float)
args = parser.parse_args()


# Open the RS485 connection
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

TIME_DELAY=args.Frequency # Change if needed. Time to sleep between samples
ION_READ="#01RD\r"
CG_READ="#01RDCG1\r"
FILENAME="/home/pi/Desktop/vacuum-logs/LOG-"+args.Filename+".csv" # Change start date to month-day

log = ""
z = open(FILENAME,'a')
z.write("Time from Epoch (s),CGn Reading (Torr),ION Gauge Reading (Torr)\n")
z.close()

begin_time = time.time()

while 1:
        z = open(FILENAME,'a')
    log = "" # clear current line
    # Get current time from Epoch
    cur_time = time.time()   # Get the current time
    log += str(cur_time)+"," # Add current time to current sample
    print "---- SAMPLE T=",cur_time," ----" # Print to terminal
    # Request a CGn reading
    ser.write(CG_READ)     # Send the read command for CG
    time.sleep(.05)        # Required wait period

    # Read CGn value
    CG_VAL = ser.read_all()     # Read the raw return value
    RAW_CG = copy.copy(CG_VAL)  # Keep raw value for log
        if CG_VAL.find("*01") > -1:  # Check for valid reading
            print "\t CGn Raw return: ",RAW_CG
               start  = CG_VAL.index("*01")+3  # Find the start of important info
                end    = CG_VAL.index('\r') # Find the end of important info
                CG_VAL = CG_VAL[start:end]  # Get the actual reading
                CG_VAL = CG_VAL.replace(" ","") # Get rid of any possible spaces
                CG = float(CG_VAL[0:4])*10**float(CG_VAL[5:]) # Parse the value
                print "\t CGn READING: ",CG, " Torr"
                log += str(CG) + ","

                # Request a ION reading
        ser.write(ION_READ)
        time.sleep(.05)
        # Read ION value
        ION_VAL = ser.read_all()
    RAW_ION = copy.copy(ION_VAL) # Keep raw response
        if ION_VAL.find("*01") > - 1: # Check for valid reading
                try:
                        print "\t ION Raw return: ",RAW_ION
                        start  = ION_VAL.index("*01")+3
                        end    = ION_VAL.index('\r')
                        ION_VAL = ION_VAL[start:end]
                        ION_VAL = ION_VAL.replace(" ","")
                        ION = float(ION_VAL[0:4])*10**float(ION_VAL[5:])
                        print "\t ION READING: ",ION_VAL, " Torr"
                        log += str(ION) + "\n"
                except Exception as e:
                        print(e)
                        print("continuing with data capture")
        z.write(copy.copy(log))
    print "\t Added entry to log file: ",FILENAME
        z.close()

    time_elapsed = int(time.time()-begin_time)
    h = time_elapsed/60/60
    m = time_elapsed/60 - h*60
    s = time_elapsed - m*60 -h*60*60
    print "\t Time Elapsed: ",h," Hours ",m," Minutes ",s," Seconds "
    print "\t **Press CTRL-C to stop logging.**\n\n\n"
    time.sleep(TIME_DELAY)
