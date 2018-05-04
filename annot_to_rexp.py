#!/usr/bin/python

import sys
from Bio import SeqIO

print "annot_to_rexp.py FastaFile AnnotationFile"

try:
    fasta_f = sys.argv[1]
except:
    fasta_f = raw_input("Introduce FASTA file with RepeatExplorer's contigs:  ")

try:
    annot_f = sys.argv[2]
except:
    annot_f = raw_input("Introduce FASTA file with RepeatExplorer's contigs:  ")

annot_dict = {}

annot = open(annot_f).readlines()

for line in annot:
    info = line.split()
    if not info[1].startswith("-"):
        annot_dict[info[0]] = info[1]


out = open(fasta_f+".annot", "w")

fasta = SeqIO.parse(open(fasta_f), "fasta")

for s in fasta:
    id = str(s.id)
    seq = str(s.seq)
    cluster = id.split("Contig")
    if cluster[0] in annot_dict:
        final_annot = annot_dict[cluster[0]]
        line = ">%s#%s\n%s\n" % (id,final_annot,seq)
        out.write(line)

out.close()
