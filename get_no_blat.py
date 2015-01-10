#!/usr/bin/python

import sys
from Bio import SeqIO

try:
    seqs = sys.argv[1]
except:
    seqs = raw_input("Introduce fasta file: ")

try:
    blat = sys.argv[2]
except:
    blat = raw_input("Introduce blat output: ")

read_seqs = SeqIO.parse(open(seqs),"fasta")
read_blat = open(blat).readlines()

list_seqs = []
list_blat = []

for s in read_seqs:
    list_seqs.append(s.id)

for b in read_blat[5:]:
    info = b.split()
    list_blat.append(info[9])

diff = set(list_seqs)^set(list_blat)

w = open(seqs+".diff","w")

w.write("\n".join(diff))

w.close()
