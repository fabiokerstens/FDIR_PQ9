#!/usr/bin/env python

import threading
import json
# import pq_module as pq
import pq_comms as pqc
import time
import signal
import sys
import random
# from PQ_integretion_testing.Defaults import json_bad, json_good
from Defaults import json_bad, json_good

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
    print "--------------------------"
    print "Ensure board reset pressed"
    print "-------------------------- \n"
    time.sleep(3)
    i = 0
    counter_sent = 0
    boot_counter = -1
    try:
        bad_addresses = json.load(open(json_bad.replace('\\', '/')))
    except:
        bad_addresses = []

    try:
        good_addresses = json.load(open(json_good.replace('\\', '/')))
    except:
        good_addresses = []
    memory_address = 0

    global working
    while working:
        # To receive ping comments, uncomment the first line, for Housekeeping uncomment the second line.

        if i >= 2:
            # Flipping a bit, all inputs must be strings
            # pq_class.ftdebug(str(536874642), "set", "255")
            # memory_address = random.randint(sram_0, sram_1)


            memory_address = random.randint(sram_int-1000, sram_int+1000)
            while memory_address in bad_addresses or memory_address in good_addresses:
                memory_address = random.randint(sram_int - 1000, sram_int + 1000)

            # memory_address = 536874742
            # memory_address = 536874642

            pq_class.ftdebug(str(memory_address), "set", "255")
            print pq_class.status, "at memory address", memory_address
            counter_sent += 1

        time.sleep(2)
        # pq_class.ping("DEBUG")
        pq_class.housekeeping("DEBUG")
        print(pq_class.status)
        counter_sent += 1
        boot_counter += 1

        time.sleep(2)

        packets = pq_class.get_packets()


        # print(packets)
        if packets:
            for packet in packets:
                # process_frame(packet)
                print("Hello from ", packet['Source'])
                if packet['Service'] == 'Housekeeping':
                    print hex(int(packet['testing2'])), hex(int(packet['testing4'])), "Counter:", packet['Counter'], \
                          "Boot counter", packet['BootCounter']
                # if i>=2 and memory_address not in good_addresses:
                #     good_addresses.append(memory_address)
                #     print len(good_addresses), "good addresses"
                #     with open(json_good, 'w') as fout:
                #         json.dump(good_addresses, fout)

                if packets[-1]['Counter'] != str(counter_sent):
                    print
                    print "Packet missing "
                    time.sleep(1)
        else:
            print "no packets"
            # working = False
            # if memory_address not in bad_addresses:
                # bad_addresses.append(memory_address)
                # print len(bad_addresses), "bad addresses"
                # with open(json_bad, 'w') as fout:
                #     json.dump(bad_addresses, fout)
            time.sleep(2)
            print "\n reset board"
            time.sleep(2)
        time.sleep(1)


        # packets = pq_class.get_packets()
        # print(packets)
        # if packets:
        #     for packet in packets:
        #         # process_frame(packet)
        #         print("Hello from ", packet['Source'])
        #         # print(packet)
        # time.sleep(5)
        i += 1
        # print "Total counter is", counter_sent, "and Boot Counter is", boot_counter
        print


# -------- Inputs ------
tcp_ip = '127.0.0.1'        # IP-address of the bus
tcp_port = 10000            # Serial port used by the bus
buffer_size = 1024          # Maximum size of the buffer (10 bit)

working = True              # Initialise the code as working

sram_0 = int("0x20000000", 16)          # SRAM memory address region lower
sram_1 = int("0x20100000", 16)          # SRAM memory address region upper
sram_int = 536874642                    # Memory address given by Nikitas


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
