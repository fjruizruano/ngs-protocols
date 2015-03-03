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
        line = line[:-1]+"#Unknown/"+line[1:]
    w.write(line)

w.close()
