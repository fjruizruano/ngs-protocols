#!/usr/bin/python

import sys
from subprocess import call

print "Usage: extract_regions_bam.py BamFile RegionsFile"

try:
    bam = sys.argv[1]
except:
    bam = raw_input("Introduce BAM file: ")

try:
    r_file = sys.argv[2]
except:
    r_file = raw_input("Introduce regions file 9name\tsequence\tbegin:end): ")

regions = open(r_file).readlines()

for region in regions:
    region = region.split()
    name = region[0]
    secu = region[1]
    coor = region[2]
    sam = "%s.%s.sam" % (bam,name)
    fasta = "%s.%s.fasta" % (bam,name)
    call("samtools view -h %s \042%s:%s\042 > %s" % (bam,secu,coor,sam), shell=True)
    o_sam = open(sam).readlines()
    f_file = open(fasta,"w")
    for line in o_sam:
        if not line.startswith("@"):
            info = line.split("\t")
            f_file.write(">%s\n%s\n" % (info[0],info[9]))
    f_file.close()
