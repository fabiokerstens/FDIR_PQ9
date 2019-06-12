import sys
import json
import matplotlib.pyplot as plt

res = []
cnt = []
cnt_num = 0

fname =sys.argv[1]
sbs = sys.argv[2]

f = open(fname,'r')

for line in f:
    try:
        d = json.loads(line)
        #print d
        if d['Source'] == sbs:
            #print d
            cnt_num += 1
            cnt.append(cnt_num)
            res.append(d['Counter'])
    except:
        break


f.close()

res = map(int, res)

plt.plot(cnt, res, 'ro')
plt.show()
