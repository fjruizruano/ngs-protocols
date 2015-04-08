#!/usr/bin/python

import sys

table = sys.argv[1]

data = open(table).readlines()

def divnuc(seq):
    total = 0
    dif = 0
    a = 0
    for i in range(0,len(seq)-1):
        a += 1
        for j in range(a,len(seq)):
            total += 1
            if seq[i] != seq[j]:
                dif += 1
    diversity = round(1.0*dif/total, 100)
    return diversity

nucs = ["A", "C", "T", "G"]

results = []

counter = 0
for line in data:
    info = line.split()
    seq = ""
    for nuc in range(0,len(nucs)):
        seq = seq +(nucs[nuc] * int(info[nuc]))
    res = divnuc(seq)
    counter += 1
    print str(counter) + " - " + str(res)
    results.append(res)

results = [str(x) for x in results]
w = open(table+".nucdiv", "w")
w.write("\n".join(results))
w.close()

