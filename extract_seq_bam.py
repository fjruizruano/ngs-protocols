#!/usr/bin/python

import sys
from subprocess import call

print "Usage: extract_seq_bam.py ListOfIndexedBamFiles ListOfSequences\n"

try:
    bams = sys.argv[1]
except:
    bams = raw_input("Introduce list of indexed BAM files: ")

try:
    seqs = sys.argv[2]
except:
    seqs = raw_input("Introduce list of Sequences: ")

bams = open(bams).readlines()

for bam in bams:
    bam = bam[:-1]
    name = bam.split(".")
    name = ".".join(name[:-1])
    print "Extracting sequences from %s " % (bam)
    call("cat %s | xargs samtools view -b %s > %s.sel.bam" % (seqs,bam,name), shell=True)
    call("samtools sort %s.sel.bam %s.sel.sort" % (name,name), shell=True)
    call("rm %s.sel.bam" % (name), shell=True)
    call("samtools index %s.sel.sort.bam" % (name), shell=True)
    print "DONE\n"
