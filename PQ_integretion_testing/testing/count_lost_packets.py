import sys
import json

def find_lost_packets(counter, sbs):
    prv = 0
    lost = 0

    for i in range(len(counter)):
        if i == 0:
            prv = counter[i]
        else:
            if counter[i] - prv != 1:
                lost += 1
                print "lost packet in:", i, prv, counter[i]
            prv = counter[i]
    print "Number of lost packets in", sbs, lost, "/", len(counter)

fname = sys.argv[1]
#sbs = sys.argv[2]

res_adb = []
res_adcs = []
res_eps = []
res_comms = []
res_obc = []

f = open(fname, 'r')

for line in f:
    d = json.loads(line)

    if d['Source'] == 'ADB':
        #print d
        res_adb.append(d['Counter'])
    elif d['Source'] == 'ADCS':
        #print d
        res_adcs.append(d['Counter'])
    elif d['Source'] == 'EPS':
        #print d
        res_eps.append(d['Counter'])
    elif d['Source'] == 'COMMS':
        #print d
        res_comms.append(d['Counter'])
    elif d['Source'] == 'OBC':
        #print d
        res_obc.append(d['Counter'])


f.close()

res_adb = map(int, res_adb)
res_adcs = map(int, res_adcs)
res_eps = map(int, res_eps)
res_comms = map(int, res_comms)
res_obc = map(int, res_obc)

find_lost_packets(res_adb, 'ADB')
find_lost_packets(res_adcs, 'ADCS')
find_lost_packets(res_eps, 'EPS')
find_lost_packets(res_comms, 'COMMS')
find_lost_packets(res_obc, 'OBC')
