#!/usr/bin/python

import sys
from subprocess import call
from os import listdir
from os.path import isfile, join

print "bam_coverage_join.py FastaReference ListOfBams"

try:
    ref = sys.argv[1]
except:
    ref = raw_input("Introduce FASTA reference: ")

try:
    li = sys.argv[2]
except:
    li = raw_input("Introduce list of BAM files: ")

bams = open(li).readlines()

to_join = []

onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]

for bam in bams:
    bam = bam[:-1]
    if bam+".var2" not in onlyfiles:
        if bam+".var" not in onlyfiles:
            print "Not found file %s.var, generating..." % bam
            call("pysamstats -f %s --type variation %s > %s.var" % (ref,bam,bam), shell=True)
        call("""tail -n +2 %s.var | awk {'print $1"&="$2"\t"$10"&="$12"&="$14"&="$16"&="$18"&="$20'}  > %s.var2""" % (bam,bam), shell=True)
        print "Not found file %s.var2, generating..." % bam
    else:
        print "Found file %s.var2, skipping." % bam
    to_join.append(bam+".var2")

print "Joining lists..."
call("join_multiple_lists_var.py %s " % " ".join(to_join), shell=True)

call("""sed 's/&=/\t/g' toico.txt > toico2.txt""", shell=True)

call("(head -n 2 toico2.txt && tail -n +3 toico2.txt | sort -k 1,1 -k 2n) > toico3.txt ", shell=True)

print "We're done!!!\n"
