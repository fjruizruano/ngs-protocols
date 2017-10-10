#!/usr/bin/python

import sys

print "Usage: unshuffle.py ListOfFastqFiles"

try:
    list = sys.argv[1]
except:
    list = raw_input("Introduce FASTQ file list: ")

li = open(list).readlines()

for file in li:
    file = file[:-1]

    data = open(file).readlines()

    name = file.split(".")
    name0 = ".".join(name[:-1])
    name1 = name0 + "_1." + name[-1]
    name2 = name0 + "_2." + name[-1]

    out1 = open(name1, "w")
    out2 = open(name2, "w")

    i = -1

    for line in data:
        i += 1
        if i%8 < 4:
            out1.write(line)
        else:
            out2.write(line)

    out1.close()
    out2.close()
