#!/usr/bin/python

import sys
from subprocess import call

print "cd_hit_count_clusters.py CdhitClstrFile MinClusterSize IdentityThreshold"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce CD-HIT's *.Clstr File: ")

try:
    minsize = int(sys.argv[2])
except:
    minsize = raw_input("Introduce Minimum Cluster Size: ")
    minsize = int(min)

try:
    minid = float(sys.argv[3])
except:
    minid = raw_input("Introduce Identity Threshold: ")
    minid = float(min)

#cd-hit-est -i dvit_selection.fasta -o dvit_selection.fasta.nr99 -c 0.99 -d 0 -T 12 -M 16000 


data = open(file).readlines()

#indexes = []
#sequences = []
#sizes = []

cluster_dict = {}

cluster_name = ""

for line in data:
    if line.startswith(">Cluster"):
        cluster_name = line[:-1]
        cluster_dict[cluster_name] = []
    else:
        seq = line.split()
        seq = seq[2]
        cluster_dict[cluster_name].append(seq[1:-3])

seqs_list = []

for el in cluster_dict:
    seqs = cluster_dict[el]
    if len(seqs) >= minsize:
        seqs_list.extend(seqs)

w = open("read_selection.txt", "w")
w.write("\n".join(seqs_list))
w.close()
