# Error graphs

import json
import matplotlib.pyplot as plt
import numpy as np

plt.xlabel('Memory address')
plt.ylabel('Error')
plt.ylim(bottom = -0.5)
plt.ylim(top = 1.5)



# json_bad = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/bad_addresses.json".replace('\\', '/')
# json_good = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/good_addresses.json".replace('\\', '/')

json_bad = r"C:\Users\Katy\Documents\Masters\Q3 Microsat Engineering\FDIR_PQ9\PQ_integretion_testing/bad_addresses.json".replace('\\', '/')
json_good = r"C:\Users\Katy\Documents\Masters\Q3 Microsat Engineering\FDIR_PQ9\PQ_integretion_testing/good_addresses.json".replace('\\', '/')

bad_addresses = json.load(open(json_bad.replace('\\', '/')))
good_addresses = json.load(open(json_good.replace('\\', '/')))


plt.scatter(bad_addresses, np.ones(len(bad_addresses)), c='r', s=4)
plt.scatter(good_addresses, np.zeros(len(good_addresses)), c='b', s=4)

# for i in len(good_addresses):
#     plt.scatter(bad_addresses[i], 0, c='r', s=4)



# plt.title('Reading vs. Time')





plt.show()