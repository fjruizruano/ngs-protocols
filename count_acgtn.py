#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: count_acgtn.py FastaFile"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input("Introduce FASTA file")

data = SeqIO.parse(open(fasta), "fasta")

w = open(fasta+".acgtn", "w")
w.write("name\tA\tC\tG\tT\tN\n")

for s in data:
    name = str(s.id)
    secuen = str(s.seq)
    a = secuen.count("A") + secuen.count("a")
    c = secuen.count("C") + secuen.count("c")
    g = secuen.count("G") + secuen.count("g")
    t = secuen.count("T") + secuen.count("t")
    n = secuen.count("N") + secuen.count("n")
    li = [a,c,g,t,n]
    lin = [str(x) for x in li]
    w.write("%s\t%s\n" % (name,"\t".join(lin)))

w.close()
