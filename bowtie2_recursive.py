#!/usr/bin/python

import sys
from subprocess import call

print "Usage: bowtie2_recursive.py ListOfFastqFiles FastaReference NumberOfThreads"

try:
    files = sys.argv[1]
except:
    files = raw_input("Introduce list of pairs of FASTQ files: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce FASTA reference: ")

try:
    threads = sys.argv[3]
    tt = int(threads)
except:
    threads = raw_input("Introduce number of threads (integer): ")

ref_name = ref.split(".")
ref_name = ".".join(ref_name[:-1])

try:
    for n in range(1,5):
        file = "%s.%s.bt2" % (ref_name,n)
        f_op = open(file)
    for n in range(1,3):
        file = "%s.rev.%s.bt2" % (ref_name,n)
        f_op = open(file)
except:
    call("bowtie2-build %s %s" % (ref, ref_name), shell=True)

data = open(files).readlines()

for n in range(0,len(data)/2):
    file1 = data[n/2][:-1]
    file2 = data[(n/2)+1][:-1]
    file_name = file1.split(".")
    if file_name[-1] == "gz":
        file_name = ".".join(file_name[:-2])
    elif file_name[-1] == "fq" or file_name[-1] == "fastq":
        file_name = ".".join(file_name[:-1])
    call("bowtie2 -p 12 --very-sensitive -x %s -1 %s -2 %s | nice -3 samtools view -bS - > %s.bam" % (ref_name,file1,file2,file_name), shell=True )
    call("samtools sort %s.bam %s_sort" % (file_name,file_name), shell=True)
    call("rm %s.bam" % (file_name), shell=True)
    call("samtools index %s_sort.bam" % (file_name), shell=True)
