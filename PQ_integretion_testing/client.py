#!/usr/bin/env python

import threading
import sys
import pq_module as pq
import pq_comms as pqc
import time
import signal
import sys

def signal_handler(sig, frame):
    global working
    working = False
    print('You pressed Ctrl+C!')
    pq_class.close()
    sys.exit(0)

def process_frame(packet):
    print("Hello from ", packet['Source'])

def get_packets():
    global working
    while working:
        pq_class.get_data()

def send_packets():
    # Function to transmit packets to the LaunchPad
    i = 0
    global working
    while working:
        # To receive ping commants, uncomment the first line, for Housekeeping
        # uncomment the second line.
        pq_class.ping("DEBUG")
        #pq_class.houskeeping("DEBUG")

        if i > 2:
            pq_class.ftdebug("536874642", "set", "255")
        time.sleep(5) # 30 sec. delay
        packets = pq_class.get_packets()
        #print(packets)
        if packets:
            for packet in packets:
                process_frame(packet)
        i += 1
        print 'i=',i
   

# IP-adress of the bus
TCP_IP = '127.0.0.1'

# Serial por tused by the bus
TCP_PORT = 10000

# Maximimum size of the buffer (10 bit)
BUFFER_SIZE = 1024

working = True

# Define the file directory in which the files are stored. This can be added in
# manually or via the command window (use sys.argv[1] in this case).
fname = 'testing.txt'
#fname = sys.argv[1]

# Maximum log period in minutes (time between two samples)
LOGPERIOD = 10

pq_class = pqc.pq(TCP_IP, TCP_PORT, 1, BUFFER_SIZE, fname, LOGPERIOD)

t=threading.Thread(target=get_packets)
t.start()

t2=threading.Thread(target=send_packets)
t2.start()

signal.signal(signal.SIGINT, signal_handler)

while 1:
   pass
