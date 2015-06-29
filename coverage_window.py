#!/usr/bin/python

import sys
from subprocess import call

print "Usage: coverage_window.py BedGraphFile FastaFile WindowSize"

try:
    bg = sys.argv[1]
except:
    bg = raw_input("Introduce BedGraph file: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce Fasta file: ")

try:
    window = sys.argv[3]
    window = int(window)
except:
    window = raw_input("Introduce window size (integer): ")
    window = int(window)

data = open(bg).readlines()

header = data[0]
header = header.split()
samples = header[3:]

try:
    fai = open(ref+".fai").readlines()
except:
    call("samtools faidx %s" % ref, shell=True)
    fai = open(ref+".fai").readlines()

lis = [0] * len(samples)

results = {}

for line in fai:
    line = line.split()
    name = line[0]
    length = int(line[1])
    results[name] = {}
    for n in range(0,(length/window)+1):
        results[name][n] = lis

for line in data[1:]:
    line = line.split()
    name = line[0]
    start = int(line[1])
    end = int(line[2])
    count = [int(i) for i in line[3:]]
    for n in range(0,end-start):
        number = start+n
        count_old = results[name][number/window]
        count_new = [x+y for x, y in zip(count_old, count)]
        results[name][number/window] = count_new

w = open(bg+".counts", "w")
w.write("Contig\tWindow\t%s\n" % "\t".join(samples))

for contig in results:
    for win in results[contig]:
        info = results[contig][win]
        info = [str(i) for i in info]
        w.write("%s\t%s\t%s\n" % (contig,str(win),"\t".join(info)))
