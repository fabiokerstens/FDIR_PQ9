import sys
import json

fname = sys.argv[1]

res_adb = []
res_adcs = []
res_eps = []
res_comms = []
res_obc = []

total_packets = 0
obc_packets = 0
adb_packets = 0
adcs_packets = 0
eps_packets = 0
comms_packets = 0

f = open(fname, 'r')

for line in f:

    d = json.loads(line)

    total_packets += 1

    if d['Source'] == 'ADB':
        adb_packets += 1
        #print d
        res_adb.append(d['Counter'])
    elif d['Source'] == 'ADCS':
        adcs_packets += 1
        #print d
        res_adcs.append(d['Counter'])
    elif d['Source'] == 'EPS':
        eps_packets += 1
        #print d
        res_eps.append(d['Counter'])
    elif d['Source'] == 'COMMS':
        comms_packets += 1
        #print d
        res_comms.append(d['Counter'])
    elif d['Source'] == 'OBC' or d['Source'] == 'DEBUG':
        obc_packets += 1
        #print d
        res_obc.append(d['Counter'])


f.close()

res_adb = map(int, res_adb)
res_adcs = map(int, res_adcs)
res_eps = map(int, res_eps)
res_comms = map(int, res_comms)
res_obc = map(int, res_obc)

print "Number of packets:", total_packets
print "Number of packets from OBC:", obc_packets
print "Number of packets from ADCS:", adcs_packets
print "Number of packets from ADB:", adb_packets
print "Number of packets from EPS:", eps_packets
print "Number of packets from COMMS:", comms_packets

# find_lost_packets(res_adb, 'ADB')
# find_lost_packets(res_adcs, 'ADCS')
# find_lost_packets(res_eps, 'EPS')
# find_lost_packets(res_comms, 'COMMS')
# find_lost_packets(res_obc, 'OBC')
