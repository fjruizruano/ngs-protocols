#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: sequence_ref_alt.py FastaFile RefAltFile"

try:
    fas = sys.argv[1]
except:
    fas = raw_input("Introduce FASTA file: ")

try:
    refalt = sys.argv[2]
except:
    refalt = raw_input("Introduce Ref-Alt File")

eq = {0:"N",1:"N",2:"A",3:"C",4:"T",5:"G"}

sequences = SeqIO.parse(open(fas), "fasta")

ra_data = open(refalt).readlines()

ra_dict = {}

for line in ra_data:
    info = line.split()
    name = info[0]
    posi = int(info[1])
    ref = int(info[2])
    ref = eq[ref]
    alt = int(info[3])
    alt = eq[alt]
    if name in ra_dict:
        ra_dict[name][posi] = [ref,alt]
    else:
        ra_dict[name] = {posi:[ref,alt]}

w = open("sequences_ref_alt.fasta", "w")

for s in sequences:
    name = str(s.id)
    seq_ref = list(str(s.seq))
    seq_alt = list(str(s.seq))
    if name in ra_dict:
        for el in ra_dict[name]:
            nucs = ra_dict[name][el]
            seq_ref[el] = nucs[0]
            seq_alt[el] = nucs[1]
    w.write(">%s_ref\n%s\n" % (name,"".join(seq_ref)))
    w.write(">%s_alt\n%s\n" % (name,"".join(seq_alt)))


w.close()
