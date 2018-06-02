#!/usr/bin/python

import sys
from subprocess import call

print "cd_hit_count_clusters.py FastaFileClustering MinClusterSize IdentityThreshold"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file for CD-HIT clustering: ")

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

percent = str(minid)
percent = percent.split(".")
percent = percent[1]

cd_com = "cd-hit-est -i %s -o %s.nr%s -c %s -d 0 -T 12 -M 16000" % (file, file, percent, str(minid))
call(cd_com, shell=True)

print "\n\nSelecting clusters...\n"

clstr_file = "%s.nr%s.clstr" % (file, percent)
data = open(clstr_file).readlines()

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

cluster_counter = 0

for el in cluster_dict:
    seqs = cluster_dict[el]
    if len(seqs) >= minsize:
        seqs_list.extend(seqs)
        cluster_counter += 1

w = open(file+".nr"+percent+"."+str(minsize)+".sel", "w")
w.write("\n".join(seqs_list))
w.close()

print "Selecting reads...\n"

extract_com = "seqtk subseq %s %s.nr%s.%s.sel > %s.nr%s.%s.sel.fasta" % (file, file, percent, str(minsize), file, percent, str(minsize))
call(extract_com, shell=True)

print "We extracted %s reads from %s clusters!\n" % (str(len(seqs_list)), str(cluster_counter))
