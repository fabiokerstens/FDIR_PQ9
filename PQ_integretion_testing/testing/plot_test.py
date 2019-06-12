import json
import matplotlib.pyplot as plt

res = []

f = open('test.log','r')

for line in f:
    d = json.loads(line)
    #print d
    if d['Source'] == 'OBC':
        #print d
        res.append(d['Counter'])

f.close()

res = map(int, res)

plt.plot(res)
plt.show()

raw_input('Press a key to exit')
