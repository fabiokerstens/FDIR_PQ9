# Error graphs

import json
import matplotlib.pyplot as plt
import numpy as np
from Defaults import json_missing_packets, json_data_errors, json_no_errors

plt.xlabel('Memory address')
plt.ylabel('Error')
plt.ylim(bottom = -0.5)
plt.ylim(top = 2.5)



# json_bad = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/bad_addresses.json".replace('\\', '/')
# json_good = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/good_addresses.json".replace('\\', '/')



no_errors = json.load(open(json_no_errors.replace('\\', '/')))
data_errors = json.load(open(json_data_errors.replace('\\', '/')))
missing_packets = json.load(open(json_missing_packets.replace('\\', '/')))


plt.scatter(data_errors, np.ones(len(data_errorss)), c='k', s=4)
plt.scatter(no_errors, np.zeros(len(no_errors)), c='b', s=4)
plt.scatter(missing_packets, 2*np.ones(len(missing_packets)), c='r', s=4)

# for i in len(good_addresses):
#     plt.scatter(bad_addresses[i], 0, c='r', s=4)



# plt.title('Reading vs. Time')





plt.show()