#!/usr/bin/python

import sys

try:
    file = sys.argv[1]
except:
    file = raw_input("Blat output file: ")

data = open(file).readlines()
reads = []

for line in data[5:]:
    line = line.split()
    reads.append(line[9][:-1])

reads_set = set(reads)

w = open("salida.txt", "w")

for r in reads_set:
    w.write("%s\n%s\n" % (r+"1", r+"2"))

w.close()
