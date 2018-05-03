#!/usr/bin/python

import sys
from subprocess import call
from os import listdir
from os.path import isfile, join

print "bam_coverage_join.py FastaReference ListOfBams [Maximum Depth (Default: 8000)]"

try:
    ref = sys.argv[1]
except:
    ref = raw_input("Introduce FASTA reference: ")

try:
    li = sys.argv[2]
except:
    li = raw_input("Introduce list of BAM files: ")

try:
    depth = sys.argv[3]
except:
    depth = 8000

bams = open(li).readlines()

to_join = []

onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]

for bam in bams:
    bam = bam[:-1]
    if bam+".var2" not in onlyfiles:
        if bam+".var" not in onlyfiles:
            print "Not found file %s.var, generating..." % bam
            call("pysamstats --max-depth=%s -f %s --type variation %s > %s.var" % (depth, ref,bam,bam), shell=True)
        call("""awk {'print $1"popeye"$2"\t"$4'} %s.var > %s.var2""" % (bam,bam), shell=True)
        print "Not found file %s.var2, generating..." % bam
    else:
        print "Found file %s.var2, skipping." % bam
    to_join.append(bam+".var2")

print "Joining lists..."
call("join_multiple_lists.py %s " % " ".join(to_join), shell=True)

call("""sed 's/popeye/\t/g' toico.txt > toico2.txt""", shell=True)

call("(head -n 1 toico2.txt && tail -n +2 toico2.txt | sort -k 1,1 -k 2n) > toico3.txt ", shell=True)
print "We're done!!!\n"
