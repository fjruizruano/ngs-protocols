#!/usr/bin/python

from subprocess import call
import sys

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce name of your bam file: ")

#to get all the reads where both mapped.
call("samtools view -b -F 12 %s > temp1.bam" % file, shell=True)

#to get all the reads that did not map, but whose mate mapped
call("samtools view -b -f 4 -F 8 %s > temp2.bam" % file, shell=True)

#to get all the reads that mapped, but whose mates did not.
call("samtools view -b -f 8 -F 4 %s > temp3.bam" % file, shell=True)

#to merge bam files and sort by name
call("samtools merge -u - temp[123].bam | samtools sort - mapped", shell=True)

#to index sorted bam file
call("samtools index mapped.bam", shell=True)

call("rm temp1.bam temp2.bam temp3.bam", shell=True)
