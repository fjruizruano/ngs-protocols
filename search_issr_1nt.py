#!/usr/bin/python

from Bio import SeqIO
from Bio.Seq import Seq
import sys

try:
    secu = sys.argv[1]
except:
    secu = raw_input("Introduce fasta file: ")

try:
    ssrs = sys.argv[2]
except:
    ssrs = raw_input("Introduce Meglecz's script .seq file: ")

secu = SeqIO.parse(open(secu),"fasta")
ssrs = open(ssrs).readlines()

di = {}

i = 0

for s in secu:
    i += 1
    line = ssrs[i]
    line = line.split(";")
    if len(line) > 4:
        motif_len = len(line[3][:-1])
        motif_start = int(line[4])
        motif = str(s.seq)
        motif = motif[motif_start-2:motif_start+motif_len-1]
        motif = motif[::-1]
        motif_r = Seq(motif)
        motif_r = str(motif_r.reverse_complement())
        motif_r = motif_r[::-1]
        if motif in di:
            di[motif] += 1
        elif motif_r in di:
            di[motif_r] += 1
        else:
            di[motif] = 1

w = open("output.txt","w")

for el in di:
    w.write("%s\t%s\n" % (el, str(di[el])))

w.close()
