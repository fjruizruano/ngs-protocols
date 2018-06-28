#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: dimerator.py FastaFile ReadLength\n"

try:
    fasta_file = sys.argv[1]
except:
    fasta_file = raw_input("Introduce FASTA file: ")

try:
    read_len = sys.argv[2]
    read_len = int(read_len)
except:
    read_len = raw_input("Introduce read length: ")
    read_len = int(read_len)

fasta = SeqIO.parse(open(fasta_file), "fasta")

out = open(fasta_file+".dim", "w")

for s in fasta:
    name = str(s.id)
    secu = str(s.seq)
    secu_dim = secu + secu
    while len(secu_dim) < 2*read_len:
        secu_dim = secu_dim + secu
    out.write(">%s\n%s\n" % (name, secu_dim))
    
out.close()
