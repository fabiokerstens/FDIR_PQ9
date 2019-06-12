import sys
import pq_module as pq
import matplotlib.pyplot as plt

res = []
fname = sys.argv[1]
sbs = sys.argv[2]
param = sys.argv[3]

f = open(fname,'r')

packets = pq.load_json(f)

f.close()

res, tm = pq.filter_housekeeping_param(packets, sbs, param)

dt = pq.cnv_to_timestep_arr(tm)

#print res

plt.plot(dt, res, 'ro')
plt.show()
