"""
Edited by Katy Blyth for Microsat Engineering
Main run file for recoding address which cause errors.

!!! In order to run this file, you need to change Defaults.py to your local directory !!!
"""

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

json_data_errors = r"address_logs/data_errors.json".replace('\\', '/')
json_missing_packets = r"address_logs/missing_packets.json".replace('\\', '/')
json_no_errors = r"address_logs/no_errors.json".replace('\\', '/')


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


# --> Function which resets the ADB by switching the EPS off and on, and resetting the counter in the process
def eps_reset():
    print "Resetting bus \n"
    pq_class.eps_bus_sw("Bus4Sw", "BUSSwOff")
    time.sleep(10)
    pq_class.eps_bus_sw("Bus4Sw", "BUSSwOn")
    counter_sent = 0

    return counter_sent


# --> Function checks the outputs of testing2 and testing 4 produced by housekeeping
def housekeeping_check(packet):
    if packet['testing2'] != "51966":
        print "Error in reading of testing 2"
        return False

    if packet['testing4'] != "3735928559":
        print "Error in reading of testing 4"
        return False

    return True


# --> Add data points to the correct data json file for plotting later
def address_list_update(memory_address, address_list, address_file):
    address_list.append(memory_address)
    with open(address_file, 'w') as fout:
        json.dump(address_list, fout)

    return address_list


# Send house keeping command to board
def house_keeping(counter_sent):
    pq_class.housekeeping(destination)
    print(pq_class.status)
    counter_sent += 1
    time.sleep(2)

    return counter_sent


# -->  Main function to transmit packets to the LaunchPad
def send_packets():

    # --->>> Initial values and constants
    destination = "ADB"         # Works with either "DEBUG" or "ADB"
    global working

    print "Initialising send packets\n"
    time.sleep(1)

    # --->>> Bus reset to ensure counter is 0 and bus is on
    counter_sent = eps_reset()

    # --->>> Generating lists to record memory addresses tested
    try:
        missing_packets = json.load(open(json_missing_packets.replace('\\', '/')))
    except:
        missing_packets = []    # Memory addresses where flipped bit causes missing packets
    try:
        data_errors = json.load(open(json_data_errors.replace('\\', '/')))
    except:
        data_errors = []        # Memory addresses where flipped bit causes data errors in housekeeping packet
    try:
        no_errors = json.load(open(json_no_errors.replace('\\', '/')))
    except:
        no_errors = []          # Memory addresses where flipped bit causes no errors


    # --->>> Initialising loop which generates and records data.
    while working:
        # Ping board and check for packet response, if none, resets
        pq_class.ping(destination)
        counter_sent += 1
        time.sleep(2)
        packets = pq_class.get_packets()

        if packets:
            # Radomising the memory address and checking it is one that hasn't already been checked
            memory_address = random.randint(sram_int-1000, sram_int+1000)
            while memory_address in missing_packets or memory_address in no_errors or memory_address in data_errors:
                memory_address = random.randint(sram_int - 1000, sram_int + 1000)

            # Using a mask to set all bits in a certain memory address to 1
            pq_class.ftdebug(destination, str(memory_address), "set", "255")
            print pq_class.status, "at memory address", memory_address
            counter_sent += 1
            time.sleep(2)

            # Requesting housekeeping to check data is still okay
            counter_sent = house_keeping(counter_sent)

            # Generating packets
            packets = pq_class.get_packets()

            if packets:
                # check correct number of packets present
                if packets[-1]['Counter'] != str(counter_sent) or len(packets) < 2:

                    print "\n Packet missing, retesting house keeping"
                    counter_sent = house_keeping(counter_sent)

                    packet_new = pq_class.get_packets()
                    if packet_new['Service'] == 'Housekeeping':

                        check = house_keeping(packet_new)
                        if check is True:
                            print
                            "House keeping good \n"
                            no_errors = address_list_update(memory_address, no_errors, json_no_errors)
                        if check is False:
                            data_errors = address_list_update(memory_address, data_errors, json_data_errors)

                    else:
                        print "Packet still missing. Resetting board"
                        missing_packets = address_list_update(memory_address, missing_packets, json_missing_packets)
                        counter_sent = eps_reset()

                else:
                    for packet in packets:
                        # checking data in house keeping packets
                        if packet['Service'] == 'Housekeeping':
                            check = housekeeping_check(packet)

                            if check is True:
                                print "House keeping good \n"
                                no_errors = address_list_update(memory_address, no_errors, json_no_errors)

                            if check is False:
                                data_errors = address_list_update(memory_address, data_errors, json_data_errors)

            else:
                print "no packets, retesting house keeping\n"
                counter_sent = house_keeping(counter_sent)

                packet_new = pq_class.get_packets()

                if packet_new['Service'] == 'Housekeeping':

                    check = house_keeping(packet_new)
                    if check is True:
                        print
                        "House keeping good \n"
                        no_errors = address_list_update(memory_address, no_errors, json_no_errors)
                    if check is False:
                        data_errors = address_list_update(memory_address, data_errors, json_data_errors)

                else:
                    print "Packets still missing. Resetting board"
                    missing_packets = address_list_update(memory_address, missing_packets, json_missing_packets)
                    counter_sent = eps_reset()


        # If ping not good, restart bus
        else:
            counter_sent = eps_reset()



# =================================
# ------------ Inputs -------------
# =================================

tcp_ip = '127.0.0.1'        # IP-address of the bus
tcp_port = 10000            # Serial port used by the bus
buffer_size = 1024          # Maximum size of the buffer (10 bit)

working = True              # Initialise the code as working

sram_0 = int("0x20000000", 16)          # SRAM memory address region lower
sram_1 = int("0x20100000", 16)          # SRAM memory address region upper
sram_int = 536874505                    # Memory address given by Nikitas


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
