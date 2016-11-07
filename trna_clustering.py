#!/usr/bin/python

import sys
from Bio import SeqIO
from subprocess import call

print "Usage: trna_clustering.py TrnaScanOutput FastaFile"

try:
    ts = sys.argv[1]
except:
    ts = raw_input("Introduce tRNAscan output: ")

try:
    seqs = sys.argv[2]
except:
    seqs = raw_input("Introduce FASTA file: ")

seqs = SeqIO.parse(open(seqs), "fasta")

# create lists

names = []
seque = []

# create a dictionary with name and sequence

print "\nCreating database..."

for a in seqs:
    names.append(a.id)
    seque.append(a.seq)

dictio = dict(zip(names, seque))


print "\nGetting tRNAs..."

ts_data = open(ts).readlines()

ts_name = ts.split(".")
ts_name = ts_name[:-1]
ts_name = ".".join(ts_name)

out = open(ts_name+"_seqs.fas", "w")

for line in ts_data[3:]:
    info = line.split()
    id = info[0]
    num = info[1]
    begin = int(info[2])-1
    end = int(info[3])
    if begin < end:
        ext_seq = dictio[id][begin:end]
    else:
        ext_seq = dictio[id][end:begin]
        ext_seq.reverse_complement()
    out.write(">%s_%s\n%s\n" % (id, num, ext_seq))

out.close()

call("cd-hit-est -T 12 -r 1 -i %s_seqs.fas -o %s_cdhit.fas -M 0 -aS 0.8 -c 0.8 -G 0 -g 1" % (ts_name,ts_name), shell=True)

print "\nDONE!"
