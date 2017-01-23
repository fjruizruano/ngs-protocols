#!/usr/bin/python

import sys
from subprocess import call

print "Usage: count_reads_bam.py ListOfBamFiles"

try:
    li = sys.argv[1]
except:
    li = raw_input("Introduce List of sorted BAM Files: ")

files = open(li).readlines()
names = []

for file in files:
    name = file[:-1]
    names.append(name+".swap")
    call("""samtools view -F 4 %s | awk {'print $3'} | uniq -c > %s""" % (name, name+".uniq"), shell=True)
    call("""awk '{t=$1; $1=$2; $2=t; print;}' %s > %s""" % (name+".uniq", name+".swap"), shell=True)
    call("rm %s" % (name+".uniq") , shell=True)

print "join_multiple_lists.py %s" % (" ".join(names))
call("join_multiple_lists.py %s" % (" ".join(names)), shell=True)
call("rm %s" % (" ".join(names)), shell=True)
