#!/usr/bin/python

import sys
from subprocess import call
import os

print "rm_cluster_external.py RepeatMaskerOutFile FastaFile PatternFile"

try:
    outfile = sys.argv[1]
except:
    outfile = raw_input("Introduce RepeatMakser OUT file: ")

try:
    fastafile = sys.argv[2]
except:
    fastafile = raw_input("Introduce FASTA file with the reads: ")

try:
    patfile = sys.argv[3]
except:
    patfile = raw_input("Introduce Pattern File: ")

seq_list = {}
pattern = open(patfile).readlines()
for line in pattern:
    seq = line.split()
    seq = seq[1]
    if seq not in seq_list:
        seq_list[seq] = []

data = open(outfile).readlines()
noheader = data[3:]

for n in range(0, len(noheader)):
    info = noheader[n]
    info = info.split()
    this_line = [info[4],info[9]]
    pair_line = []
    if this_line[0][-1] == "1":
        read = info[4][:-1] + "2"
        pair_line = [read,info[9]]
    elif this_line[0][-1] == "2":
        read = info[4][:-1] + "1"
        pair_line = [read,info[9]]
    sub = noheader[n-3:n] + noheader[n+1:n+4]
    up_down = []
    for el in sub:
        sub_info = el.split()
        up_down.append([sub_info[4],sub_info[9]])
    if pair_line not in up_down:
        seq_list[this_line[1]].append(pair_line[0])
#        print this_line

call("mkdir sel_reads", shell=True)
os.chdir("sel_reads")

for el in seq_list:
    out = open(el+".txt","w")
    li = seq_list[el]
    out.write("\n".join(li))
    out.close()
    call("seqtk subseq %s %s > %s" % ("../"+fastafile,el+".txt", el+".fasta"), shell=True)
    call("cd-hit-est -T 12 -i %s -r 1 -M 0 -c 0.8 -o %s" % (el+".fasta", el+".nr80"), shell=True)

