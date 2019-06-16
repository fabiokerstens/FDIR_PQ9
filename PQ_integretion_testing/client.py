#!/usr/bin/env python

import threading
import sys
# import pq_module as pq
import pq_comms as pqc
import time
import signal
import sys
import random

# -------- Functions --------


def signal_handler(sig, frame):
    global working
    working = False
    print('You pressed Ctrl+C!')
    pq_class.close()
    sys.exit(0)


# def process_frame(packet):
#     print("Hello from ", packet['Source'])


def get_packets():
    global working
    while working:
        pq_class.get_data()


def send_packets():
    # Function to transmit packets to the LaunchPad
    i = 0
    global working
    while working:
        # To receive ping comments, uncomment the first line, for Housekeeping uncomment the second line.
        pq_class.ping("DEBUG")
        print(pq_class.status)

        time.sleep(3)
        
        # pq_class.housekeeping("DEBUG")
        packets = pq_class.get_packets()


        print(packets)
        if packets:
            for packet in packets:
                # process_frame(packet)
                print("Hello from ", packet['Source'])
                # print(packet)

        time.sleep(3)

        if i >= 2:
            # Flipping a bit, all inputs must be strings
            # pq_class.ftdebug(str(536874642), "set", "255")
            memory_address = random.randint(sram_0, sram_1)
            # memory_address = 536874742
            pq_class.ftdebug(str(memory_address), "set", "255")
            print(pq_class.status)

        # packets = pq_class.get_packets()
        # print(packets)
        # if packets:
        #     for packet in packets:
        #         # process_frame(packet)
        #         print("Hello from ", packet['Source'])
        #         # print(packet)
        # time.sleep(5)
        i += 1
        print 'i=', i


# -------- Inputs ------
tcp_ip = '127.0.0.1'        # IP-address of the bus
tcp_port = 10000            # Serial port used by the bus
buffer_size = 1024          # Maximum size of the buffer (10 bit)

working = True              # Initialise the code as working

sram_0 = int("0x20000000", 16)          # SRAM memory address region lower
sram_1 = int("0x20100000", 16)          # SRAM memory address region upper


# Define the file directory in which the files are stored. This can be added in manually or via the command window (use sys.argv[1] in this case).
file_name = 'testing.txt'
# file_name = sys.argv[1]

# Maximum log period in minutes (time between two samples)
log_period = 10

pq_class = pqc.pq(tcp_ip, tcp_port, 1, buffer_size, file_name, log_period)

t = threading.Thread(target=get_packets)
t.start()

t2 = threading.Thread(target=send_packets)
t2.start()

signal.signal(signal.SIGINT, signal_handler)

while 1:
   pass
