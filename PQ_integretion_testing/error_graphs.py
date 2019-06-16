# Error graphs

import json
import matplotlib as plt

plt.xlabel('Memory address')
plt.ylabel('Error')


json_bad = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/bad_addresses.json".replace('\\', '/')
json_good = r"/home/katy/FDIR_PQ9/PQ_integretion_testing/good_addresses.json".replace('\\', '/')

bad_addresses = json.load(open(json_bad.replace('\\', '/')))
good_addresses = json.load(open(json_good.replace('\\', '/')))

for i in len(bad_addresses):
    plt.scatter(bad_addresses[i], 1, c='r', s=4)

for i in len(good_addresses):
    plt.scatter(bad_addresses[i], 0, c='r', s=4)



# plt.title('Reading vs. Time')





plt.show()