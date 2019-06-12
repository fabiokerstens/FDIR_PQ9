import sys
import pq_module as pq
import matplotlib.pyplot as plt

res = []
fname = sys.argv[1]

f = open(fname,'r')

packets = pq.load_json(f)

f.close()

sbs = ['OBC', 'ADCS', 'ADB', 'EPS', 'COMMS']
sbs_boot = [ 'ADCS', 'EPS']
sbs_id = { 'OBC' : 1, 'ADCS' : 5, 'ADB' : 3, 'EPS' : 2, 'COMMS' : 4}



param = 'Counter'
i = 0

for sb in sbs:
    plt.subplot(5, 1, i)
    plt.ylabel(sb)
    res, tm = pq.filter_housekeeping_param(packets, sb, param)
    dt = pq.cnv_to_timestep_arr(tm)
    plt.plot(dt, res)
    i += 1

plt.show()


param = 'BootCounter'
i = 0

for sb in sbs_boot:
    plt.subplot(3, 1, i)
    plt.ylabel(sb)
    res, tm = pq.filter_housekeeping_param(packets, sb, param)
    dt = pq.cnv_to_timestep_arr(tm)
    plt.plot(dt, res)
    i += 1

plt.subplot(3, 1, i)
plt.ylabel('OBC')
res, tm = pq.filter_housekeeping_rf_param(packets, sbs_id['OBC'], param)
dt = pq.cnv_to_timestep_arr(tm)
plt.plot(dt, res)
i += 1

plt.show()

param = 'Counter'
i = 0

for sb in sbs:
    plt.subplot(8, 1, i)
    plt.ylabel(sb)
    res, tm = pq.filter_housekeeping_param(packets, sb, param)
    dt = pq.cnv_to_timestep_arr(tm)
    plt.plot(dt, res)
    i += 1

param = 'BootCounter'

for sb in sbs_boot:
    plt.subplot(8, 1, i)
    plt.ylabel(sb)
    res, tm = pq.filter_housekeeping_param(packets, sb, param)
    dt = pq.cnv_to_timestep_arr(tm)
    plt.plot(dt, res)
    i += 1

plt.subplot(8, 1, i)
plt.ylabel('OBC')
res, tm = pq.filter_housekeeping_rf_param(packets, sbs_id['OBC'], param)
dt = pq.cnv_to_timestep_arr(tm)
plt.plot(dt, res)
i += 1

plt.show()
