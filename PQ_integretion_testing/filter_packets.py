import sys
import pq_module as pq

res = []
fname = sys.argv[1]
sname = sys.argv[2]
sbs = sys.argv[3]
param = sys.argv[4]

f = open(fname,'r')

packets = pq.load_json(f)

f.close()

res, tm = pq.filter_param(packets, sbs, param)

dt = pq.cnv_to_timestep_arr(tm)
