import sys
import pq_module as pq

fname =sys.argv[1]
try:
    sys.argv[2]
    debug = True
except IndexError:
    debug = False

f = open(fname,'r')

packets = pq.load_json(f)

f.close()

total_packets = pq.find_num_packets(packets, 'all')

sbs_id = { 'OBC' : 1, 'ADCS' : 5, 'ADB' : 3, 'EPS' : 2, 'COMMS' : 4}

sbs = ['OBC', 'ADCS', 'ADB', 'EPS', 'COMMS']
sbs_slaves = [ 'ADCS', 'ADB', 'EPS', 'COMMS']
sbs_ev = ['all', 'OBC', 'ADCS', 'ADB', 'EPS', 'COMMS']

services = ['all', 'Housekeeping', 'Ping']

print "Number of packets:"

for sb in sbs:
    res = pq.find_num_packets(packets, sb)
    print  res, "/", total_packets, "in", sb

print "Number of lost packets:"

for sb in sbs:
    pq.find_lost_packets(packets, sb, debug)

print "Number of requests/responses:"

for srv in services:
    for sb in sbs_slaves:
        pq.find_request_response(packets, sb, srv)

print "Number of RF packets:"

for sb in sbs:
    pq.find_rf_packets(packets, sb, sbs_id[sb])

print "Number of resets (boot counter):"

for sb in sbs_slaves:
    pq.find_boot_counter_resets(packets, sb, debug)

print "Number of resets (packet counter):"

for sb in sbs:
    pq.find_packet_counter_resets(packets, sb, debug)


print "Packet timings in seconds:"

for sb in sbs_ev:
    pq.find_packets_time_stats(packets, sb)
