#!/usr/bin/python

import sys
from subprocess import call

print "Usage: ssaha2.py ListOfFiles Reference"

try:
    files = sys.argv[1]
except:
    files = raw_input("Introduce list of files: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce FASTA reference: ")

refp = ref.split(".")
refpoints = refp[0:-1]
refname = ".".join(refpoints)

try:
    test = open(refname+".head")
    test = open(refname+".body")
    test = open(refname+".size")
    test = open(refname+".name")
    test = open(refname+".base")
except:
    call("ssaha2Build -solexa -save %s %s" % (refname, ref), shell=True)

try:
    test = open(ref+".fai")
except:
    call("samtools faidx %s" % (ref), shell=True)

files = open(files).readlines()

for n in range(0,len(files)/2):
    file1 = files[n*2][:-1]
    file2 = files[(n*2)+1][:-1]
#    filepoints

#    call("ssaha2 -solexa  -pair 20,400 -identity 80 -output sam -outfile %s -best 1 -save %s %s %s" % (file1+".sam",refname,file1,file2), shell=True)
    call("ssaha2 -solexa  -pair 20,400 -score 40 -identity 80 -output sam -outfile %s -best 1 -save %s %s %s" % (file1+".sam",refname,file1,file2), shell=True)
    call("samtools view -bt %s.fai %s > %s" % (ref,file1+".sam",file1+".bam"), shell=True)
    call("rm %s" % (file1+".sam"), shell=True)
    call("samtools sort %s %s" % (file1+".bam", file1+".sort"), shell=True)
    call("rm %s" % (file1+".bam"), shell=True)
    call("reduce_bam.py %s" % (file1+".sort.bam"), shell=True)
    call("rm %s" % (file1+".sort.bam"), shell=True)
