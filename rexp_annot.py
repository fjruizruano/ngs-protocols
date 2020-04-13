#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: rexp_annot.py RexpFastaFile AnnotationFile [Unknown]"

try:
    ff = sys.argv[1]
except:
    ff = raw_input("Introduce FASTA file from RepeatExplorer assembly: ")

try:
    aa = sys.argv[2]
except:
    aa = raw_input("Introduce Annotation File: ")

try:
    uu = sys.argv[3]
except:
    uu = ""

annots = open(aa).readlines()
annotations = {}

for annot in annots:
    annot = annot.split()
    if len(annot) > 0:
        cl = annot[0]
        try:
            fam = annot[1]
            annotations[cl] = fam
        except:
            pass

if uu == "Unknown":
    out = open(ff+".annot.unknown", "w")
else:
    out = open(ff+".annot", "w")

seqs = SeqIO.parse(open(ff), "fasta")

for s in seqs:
    name = s.id
    cluster = name.split("Contig")
    cluster = cluster[0]
    if cluster in annotations:
        out.write(">%s#%s\n%s\n" % (name,annotations[cluster],str(s.seq)))
    elif uu == "Unknown":
        out.write(">%s#Unknown\n%s\n" % (name,str(s.seq)))

out.close()
