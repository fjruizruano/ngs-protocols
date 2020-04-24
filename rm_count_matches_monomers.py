#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: rm_count_matches.py FastaFile MinimumLength\n"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input ("Introduce FastaFile: ")

try:
    minlen = sys.argv[2]
except:
    minlen = raw_input ("Introduce MinimumLength: ")

seqs = SeqIO.parse(open(fasta),"fasta")

counter_dim = {}
counter_nodim = {}

for seq in seqs:
    secu = str(seq.seq)
    id = str(seq.id)
    info = id.split("_")
    read = info[1]
    annot = info[0]
#    mono_len = annot
#    mono_len = mono_len.split("-")
#    mono_len = int(mono_len[1])

    if annot not in counter_dim:
        counter_dim[annot] = [0,0]
        counter_nodim[annot] = [0,0]

    if len(secu) > minlen: # previously 89
        a = counter_dim[annot][0]
        b = counter_dim[annot][1]
        counter_dim[annot] = [a+1,b+len(secu)]
    else:
        a = counter_nodim[annot][0]
        b = counter_nodim[annot][1]
        counter_nodim[annot] = [a+1,b+len(secu)]

out = open(fasta+".counts", "w")
out.write("Annotation\tDIM_N\tDIM_MON\tNODIM_N\tNODIM_MON\n")

for el in sorted(counter_dim):
    dim = counter_dim[el]
    nodim = counter_nodim[el]
    lili = dim+nodim
    lili = [str(i) for i in lili]
    lili = [el]+lili
    out.write("\t".join(lili)+"\n")
