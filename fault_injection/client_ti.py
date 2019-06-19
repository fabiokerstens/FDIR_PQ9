#!/usr/bin/env python

import threading
import json
import pq_comms as pqc
import time
import signal
import sys
import random


# ===================================
# ------- Loading .json files -------
# ===================================

json_data_errors = r"address_logs/data_errors_ti.json".replace('\\', '/')
json_missing_packets = r"address_logs/missing_packets_ti.json".replace('\\', '/')
json_no_errors = r"address_logs/no_errors_ti.json".replace('\\', '/')

# =================================
# ----------- Functions -----------
# =================================


def signal_handler(sig, frame):
    global working
    working = False
    print('You pressed Ctrl+C!')
    pq_class.close()
    sys.exit(0)


def get_packets():
    global working
    while working:
        pq_class.get_data()


# --->> Checks house keeping packet is correct
# Can add more parameter checks when using a board with more fixed inputs
def housekeeping_check(packet, boot_counter):
    if packet['DBGSW1'] != "OFF" or packet['DBGSW2'] != "OFF":
        print "Error in board button reading"
        return False
    if packet['testing4'] != "3735928559" or packet['testing2'] != "51966":
        print "Error in reading of testing 2 or 4"
        return False
    print hex(int(packet['testing2'])), hex(int(packet['testing4']))
    if packet['SoftwareBootCounter'] != str(0):
        print "Error in software boot counter"
        return False
    if str(boot_counter) != packet['BootCounter']:
        print "Error in boot counter"
        return False
    return True

# --> Add data points to the correct data json file for plotting later
def address_list_update(memory_address, address_list, address_file):
    address_list.append(memory_address)
    with open(address_file, 'w') as fout:
        json.dump(address_list, fout)

    return address_list

# -->  Main function to transmit packets to the LaunchPad
def send_packets():
    # Function to transmit packets to the LaunchPad
    print "--------------------------"
    print "Ensure board reset pressed"
    print "-------------------------- \n"
    time.sleep(3)

    # --->>> Generating lists to record memory addresses tested
    try:
        missing_packets = json.load(open(json_missing_packets.replace('\\', '/')))
    except:
        missing_packets = []
    try:
        data_errors = json.load(open(json_data_errors.replace('\\', '/')))
    except:
        data_errors = []
    try:
        no_errors = json.load(open(json_no_errors.replace('\\', '/')))
    except:
        no_errors = []

    # Setting initial values
    i = 0
    counter_sent = 0
    boot_counter = -1
    memory_address = 0
    global working
    while working:
        # To receive ping comments, uncomment the first line, for Housekeeping uncomment the second line.

        if i >= 2:
            # Flipping a bit, all inputs must be strings
            memory_address = random.randint(sram_0, sram_int + 100000)
            while memory_address in missing_packets or memory_address in no_errors or memory_address in data_errors:
                memory_address = random.randint(sram_0, sram_int + 100000)

            pq_class.ftdebug("DEBUG", str(memory_address), "set", "255")
            print pq_class.status, "at memory address", memory_address
            counter_sent += 1

        time.sleep(2)
        pq_class.housekeeping("DEBUG")
        print(pq_class.status)

        counter_sent += 1
        boot_counter += 1
        time.sleep(2)

        packets = pq_class.get_packets()

        if packets:
            if packets[-1]['Counter'] != str(counter_sent):
                print
                print "Packet missing "

                missing_packets = address_list_update(memory_address, missing_packets, json_missing_packets)

                time.sleep(1)
                print "\n reset board"
                time.sleep(3)
                boot_counter = -1
                counter_sent = 0

            else:
                for packet in packets:
                    print("Hello from ", packet['Source'])
                    if packet['Service'] == 'Housekeeping':
                        check = housekeeping_check(packet, boot_counter)
                        if check is True and i>=2:
                            no_errors = address_list_update(memory_address, no_errors, json_no_errors)

                        if check is False and i>=2:
                            data_errors = address_list_update(memory_address, data_errors, json_data_errors)
        else:
            missing_packets = address_list_update(memory_address, missing_packets, json_missing_packets)
            print "no packets \n"
            time.sleep(1)
            print "reset board"
            boot_counter = -1
            counter_sent = 0
            time.sleep(3)
        time.sleep(1)

        i += 1

        print


# =================================
# ------------ Inputs ------------
# =================================

tcp_ip = '127.0.0.1'        # IP-address of the bus
tcp_port = 10000            # Serial port used by the bus
buffer_size = 1024          # Maximum size of the buffer (10 bit)

working = True              # Initialise the code as working

sram_0 = int("0x20000000", 16)          # SRAM memory address region lower
sram_1 = int("0x20100000", 16)          # SRAM memory address region upper
sram_int = 536874642                    # Memory address known to give a bit flip error

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
