#!/usr/bin/python

import sys

print "cd_hit_count_clusters.py CdhitClstrFile MinClusterSize MaxClusterSize"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce CD-HIT's *.Clstr File: ")

try:
    min = int(sys.argv[2])
except:
    min = raw_input("Introduce Minimum Cluster Size:")
    min = int(min)

try:
    max = int(sys.argv[3])
except:
    max = raw_input("Introduce Maximum Cluster Size:")
    max = int(min)

data = open(file).readlines()

indexes = []
sequences = []
sizes = []

for n in range(0,len(data)):
    if data[n].startswith(">Cluster"):
        indexes.append(n)
    elif data[n].endswith("*\n"):
        info = data[n]
        info = info.split()
        info = info[2][1:-3]
        sequences.append(info)

for n in range(0,len(indexes)):
    if n != len(indexes)-1:
        info = data[indexes[n+1]-1]
    else:
        info = data[-1]
    info = info.split()
    info = int(info[0])+1
    sizes.append(info)

w = open(file+".sel.%s.%s" % (str(min), str(max)), "w")

ww = open(file+".clu.%s.%s" % (str(min), str(max)), "w")

for n in range(0, len(sizes)):
    if sizes[n] >= min and sizes[n] <= max:
        w.write("%s\n" % sequences[n])
        cluster = data[indexes[n]:indexes[n+1]]
        uniq_cluster = []
        for el in cluster[1:]:
            i = el.split("\t")
            uniq_cluster.append(i[1])
        uniq_cluster = set(uniq_cluster[1:])
        uniq_cluster = list(uniq_cluster)
        ucl = len(uniq_cluster)
        if ucl >= min and ucl <= max:
            ww.write(cluster[0]+"".join(uniq_cluster))

print el 
print i
print i[1:]
print uniq_cluster

w.close()
ww.close()


