#!/usr/bin/python

import sys
from subprocess import call

print "Usage: fastq_paired_combine_id.py file_1.fastq file_2.fastq"

try:
    one = sys.argv[1]
except:
    one = raw_input("Introduce FASTQ file 1: ")

try:
    two = sys.argv[1]
except:
    two = raw_input("Introduce FASTQ file 2: ")

get_reads = """awk 'NR == 1 || NR % 4 == 1' """
trim_reads = """awk '{print substr($1,2, length($0)-3)}' """

files = sys.argv[1:3]

print "Getting read names"
for file in files:
    call(get_reads + "%s > %s" % (file, file+".r"), shell=True)
    call(trim_reads + "%s > %s" % (file+".r", file+".t"), shell=True)
    call("rm %s" % (file+".r"), shell=True)

one_data = open(files[0]+".t").readlines()
two_data = open(files[1]+".t").readlines()

print "Getting commun reads"
commun = set(one_data) & set(two_data)

call("rm %s.t %s.t" % (files[0], files[1]), shell=True)

name = files[0]
name = name.split(".")
name = ".".join(name[:-1])
name = name[:-2]

out = open(name+".list", "w")
for el in commun:
    out.write("%s/1\n%s/2\n" % (el[:-1], el[:-1]))
out.close()

print "Extracting reads from original files"
call("seqtk subseq %s %s.list > %s_paired_1.fastq" % (one,name,name), shell=True)
call("seqtk subseq %s %s.list > %s_paired_2.fastq" % (two,name,name), shell=True)

call("call %s.list" % (name), shell=True)

print "We're done!"
