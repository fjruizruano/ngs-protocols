#!/usr/bin/python

import sys
from subprocess import call

print "Usage: bg_count.py ListOfBamFiles Reference"

try:
    li = sys.argv[1]
except:
    li = raw_input("Introduce List of indexed BAM files: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce Reference in FASTA format: ")

files = open(li).readlines()

li_bg = []
li_names = []

for file in files:
    file = file[:-1]
    li_bg.append(file+".bg")
    name = file.split(".")
    li_names.append(name[0])
    call("genomeCoverageBed -bg -ibam %s > %s.bg" % (file,file), shell=True)

call("unionBedGraphs -header -i %s -names %s -g %s -empty > samples1and2.txt" % (" ".join(li_bg), " ".join(li_names), ref+".fai"), shell=True)

call("coverage_seq_bed.py samples1and2.txt", shell=True)
