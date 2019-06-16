import sys
import pq_module as pq
import matplotlib.pyplot as plt

res = []

# Directory of the file where the packets are stored.
fname = sys.argv[1]
sbs = sys.argv[2]
param = sys.argv[3]

# Read the file
f = open(fname,'r')

# The entries in the file are in JSON format. This command converts the commands
# back to packet files.
packets = pq.load_json(f)

# Close the file. 
f.close()

res, tm = pq.filter_housekeeping_param(packets, sbs, param)

dt = pq.cnv_to_timestep_arr(tm)

plt.plot(dt, res, 'ro')
plt.show()
