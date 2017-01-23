#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: dnapipete_createdb.py Trinity.fasta one_RM_hit_per_Trinity_contigs [unknown]"

try:
    trinity = sys.argv[1]
except:
    trinity = raw_input("Introduce path the Trinity.fasta file: ")

try:
    annot = sys.argv[2]
except:
    annot = raw_input("Introduce path to the one_RM_hit_per_Trinity_contigs file: ")

try:
    unknownq = sys.argv[3]
except:
    unknownq = ""

secus = SeqIO.parse(open(trinity),"fasta")
annot_read = open(annot).readlines()
annotations = {}

for annotation in annot_read:
    annotation = annotation.split()
    annotations[annotation[0]] = annotation[4]

w = open("Trinity.annot.fasta","w")

for sec in secus:
    name = ""
    if sec.id in annotations:
        name = "%s#%s" % (sec.id, annotations[sec.id])
        w.write(">%s\n%s\n" % (name, str(sec.seq)))
    elif unknownq != "":
        name = "%s#Unknown" % (sec.id)
        w.write(">%s\n%s\n" % (name, str(sec.seq)))

w.close()
