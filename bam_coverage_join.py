#!/usr/bin/python

import sys
from subprocess import call

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

for bam in bams:
    bam = bam[:-1]    
    call("pysamstats -f %s --type variation %s > %s.var" % (ref,bam,bam), shell=True)
    call("""awk {'print $1"popeye"$2"\t"$4'} %s.var > %s.var2""" % (bam,bam), shell=True)
    to_join.append(bam+".var2")

call("join_multiple_lists.py %s " % " ".join(to_join), shell=True)

call("(head -n 1 toico.txt && tail -n +2 toico.txt | sort) > toico2.txt ", shell=True)

call("""sed 's/popeye/\t/g' toico2.txt > toico3.txt""", shell=True)
