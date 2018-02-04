#!/usr/bin/python

import sys

print "Usage: rm_count_matches.py FastaFile\n"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input ("Introduce FastaFile: ")

data = open(fasta).readlines()

list_reads = []

counter_all = {}
counter_double = {}

for line in data:
    if line.startswith(">"):
        info = line[1:-2]
        info = info.split("_")
        annot = info[0]
        read = info[1]

        if annot not in counter_all:
            counter_all[annot] = 0
            counter_double[annot] = 0

        if read in list_reads:
            counter_double[annot] += 2
            counter_all[annot] += 1
        else:
            list_reads.append(read)
            counter_all[annot] += 1

out = open(fasta+".counts", "w")
out.write("Annotation\tAll\tPaired\n")

for el in counter_all:
    all = str(counter_all[el])
    double = str(counter_double[el])
    lili = [el,all,double]
    out.write("\t".join(lili)+"\n")
