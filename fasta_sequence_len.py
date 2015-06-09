#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: fasta_sequence_len.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file: ")

data = SeqIO.parse(open(file), "fasta")

w = open(file+".len", "w")

for s in data:
    w.write("%s\t%s\n" % (str(s.id), len(str(s.seq))))

w.close()
