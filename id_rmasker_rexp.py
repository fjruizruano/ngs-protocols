#!/usr/bin/python

import sys

try:
    file = sys.argv[1]
except:
    print "Usage: id_rmasker.py FastaFile"

data = open(file).readlines()

w = open(file+".rmasker", "w")

for line in data:
    if line.startswith(">"):
        line = line.split(" ")
        cl = line[0]
        cl = cl.split("Contig")
        line = line[0]+"#Unknown/"+cl[0][1:]+"\n"
    w.write(line)

w.close()
