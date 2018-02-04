#!/usr/bin/python

import sys
from Bio import SeqIO

print "Usage: ecopcr_db.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce Fasta file: ")

data = SeqIO.parse(open(file), "fasta")

out = open(file+".mod", "w")

for s in data:
    secu = str(s.seq)
    name = str(s.id)
    sp_name = ""
    fam_name = ""
    info = s.description
    info = info.split("; ")
    for el in info:
        if el.startswith("species_name="):
            sp_name = el
            sp_name = sp_name.split("=")
            sp_name = sp_name[1]
            sp_name = sp_name.replace(" ","_")
        if el.startswith("family_name="):
            fam_name = el
            fam_name = fam_name.split("=")
            fam_name = fam_name[1]
    out.write(">%s_%s_%s\n%s\n" % (name,sp_name,fam_name,secu))
out.close()
