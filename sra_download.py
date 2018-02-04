#!/usr/bin/python

import sys
from subprocess import call

print "sra_download.py ListOfSRAAccessionNumbers"

try:
    li = sys.argv[1]
except:
    li = raw_input("Introduce list of SRA Accession Numbers")

data = open(li).readlines()

for line in data:
    acc = line[:-1]
    url = "ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra" % (acc[0:3], acc[0:6], acc, acc)
    print url
    call("wget %s" % (url), shell = True)
