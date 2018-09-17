#!/usr/bin/python

from subprocess import call
import sys

print "Usage: reduce_bam.py BamFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce name of your bam file: ")

name = file.split(".")
name = name[0]

print "\nReducing file %s..." % (file)

#to get all the reads where both mapped.
call("samtools view -b -F 12 %s > temp1.bam" % file, shell=True)

#to get all the reads that did not map, but whose mate mapped
call("samtools view -b -f 4 -F 8 %s > temp2.bam" % file, shell=True)

#to get all the reads that mapped, but whose mates did not.
call("samtools view -b -f 8 -F 4 %s > temp3.bam" % file, shell=True)

#to merge bam files and sort by name
#call("samtools merge -u - temp[123].bam | samtools sort - %s_mapped" % (name), shell=True)
call("samtools merge -u - temp[123].bam | samtools sort -T aln.sorted - -o %s_mapped.bam" % (name), shell=True) 


#to index sorted bam file
call("samtools index %s_mapped.bam" % (name), shell=True)

call("rm temp1.bam temp2.bam temp3.bam", shell=True)
