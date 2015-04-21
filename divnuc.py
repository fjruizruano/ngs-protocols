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
    try:
        diversity = round(1.0*dif/total, 100)
    except:
        diversity = 0
    return diversity

nucs = ["D","I","A", "C", "T", "G"]

w = open(table+".divnuc", "w")

counter = 0
for line in data:
    info = line.split()
    seq = ""
    for nuc in range(0,len(nucs)):
        seq = seq +(nucs[nuc] * int(info[nuc+3]))
    res = divnuc(seq)
    counter += 1
    print str(counter) + " - " + str(res)
    info.append(res)
    info = [str(x) for x in info]
    w.write("\t".join(info)+"\n")

w.close()

