#!/usr/bin/python

import sys
from Bio import SeqIO

print "remove_ns.py MaskedFastaFile"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input("Introduce masked FASTA file: ")

data = SeqIO.parse(open(fasta), "fasta")

out = open(fasta+".withoutn", "w")

for s in data:
    secu = str(s.seq)
    if secu.find("N") == -1:
        out.write(">%s\n%s\n" % (str(s.id), secu))

out.close()
