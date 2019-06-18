# Error graphs

import json
import matplotlib.pyplot as plt
import numpy as np

# Loading .json files
json_data_errors = r"address_logs/data_errors.json".replace('\\', '/')
json_missing_packets = r"address_logs/missing_packets.json".replace('\\', '/')
json_no_errors = r"address_logs/no_errors.json".replace('\\', '/')


plt.xlabel('Memory address')
plt.ylabel('Error')
plt.ylim(bottom = -0.5)
plt.ylim(top = 2.5)



no_errors = json.load(open(json_no_errors.replace('\\', '/')))
data_errors = json.load(open(json_data_errors.replace('\\', '/')))
missing_packets = json.load(open(json_missing_packets.replace('\\', '/')))

# Plotting errors for different memory location
plt.scatter(data_errors, np.ones(len(data_errorss)), c='k', s=4)
plt.scatter(no_errors, np.zeros(len(no_errors)), c='b', s=4)
plt.scatter(missing_packets, 2*np.ones(len(missing_packets)), c='r', s=4)


plt.show()