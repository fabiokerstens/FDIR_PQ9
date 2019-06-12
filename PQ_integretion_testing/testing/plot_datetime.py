import sys
import json

fname = sys.argv[1]

cnt = 0

f = open(fname, 'r')

for line in f:

    d = json.loads(line)
    cnt += 1
    print cnt, d['_timestamp_']



f.close()
