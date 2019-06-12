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
    print "Hello from ", packet['Source']

def get_packets():
    global working
    while working:
        pq_class.get_data()

def send_packets():
    global working
    while working:
        pq_class.ping("OBC")
        time.sleep(30)
        packets = pq_class.get_packets()
        #print packets
        if packets:
            for packet in packets:
                process_frame(packet)

TCP_IP = '127.0.0.1'
TCP_PORT = 10000
BUFFER_SIZE = 1024

working = True

fname = sys.argv[1]

pq_class = pqc.pq(TCP_IP, TCP_PORT, 1, BUFFER_SIZE, fname, 10)

t=threading.Thread(target=get_packets)
t.start()

t2=threading.Thread(target=send_packets)
t2.start()

signal.signal(signal.SIGINT, signal_handler)

while 1:
   pass
