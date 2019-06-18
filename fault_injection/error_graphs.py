# Error graphs

import json
import matplotlib.pyplot as plt
import numpy as np

# Loading .json files

# ---- ADB DATA ----
# json_data_errors = r"address_logs/data_errors.json".replace('\\', '/')
# json_missing_hk_packets = r"address_logs/missing_hk_packets.json".replace('\\', '/')
# json_missing_ft_packets = r"address_logs/missing_ft_packets.json".replace('\\', '/')
# json_no_errors = r"address_logs/no_errors.json".replace('\\', '/')

# --- TI Board DATA ---
json_missing_packets = r"address_logs/missing_packets_ti.json".replace('\\', '/')
json_no_errors = r"address_logs/no_errors_ti.json".replace('\\', '/')

plt.xlabel('Memory address')
plt.ylabel('Error')
plt.ylim(bottom = -0.5)
plt.ylim(top = 1.5)



no_errors = json.load(open(json_no_errors.replace('\\', '/')))
# data_errors = json.load(open(json_data_errors.replace('\\', '/')))
missing_packets = json.load(open(json_missing_packets.replace('\\', '/')))
# missing_hk_packets = json.load(open(json_missing_hk_packets.replace('\\', '/')))

# Plotting errors for different memory location
# plt.scatter(data_errors, np.ones(len(data_errorss)), c='k', s=4)
plt.scatter(no_errors, np.zeros(len(no_errors)), c='b', s=4)
plt.scatter(missing_packets, np.ones(len(missing_packets)), c='r', s=4)
print(len(no_errors)+len(missing_packets))

plt.show()