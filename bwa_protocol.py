#!/usr/bin/python

import sys
from subprocess import call

print "\nUsage: bwa_protocol.py ListOfReads Reference Threads [noreduce/reduce]\n"

try:
    data = sys.argv[1]
except:
    data = raw_input("List of reads: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("FASTA reference file: ")

try: 
    threads = sys.argv[3]
except:
    threads = raw_input("Number of threads: ")

try:
    reduce = sys.argv[4]
except:
    reduce = raw_input("Reduce or not reduce: ")

files = open(data).readlines()
l_files = []
for f in range(0,(len(files)/2)):
    l_files.append([files[f*2][:-1],files[(f*2)+1][:-1]])

try:
	open(ref+".pac")
	open(ref+".ann")
	open(ref+".amb")
	open(ref+".bwt")
	open(ref+".sa")
except:
	call("bwa index -a bwtsw %s" % ref, shell=True)

for pair in l_files:
    name = pair[0]
    name = name.split(".")
    name = name[0][:-2]
    call("bwa aln -t%s %s %s > read1.sai" % (threads, ref, pair[0]), shell=True)
    call("bwa aln -t%s %s %s > read2.sai" % (threads, ref, pair[1]), shell=True)
    call("bwa sampe -s -r \042@RG\tID:1\tLB:1\tSM:1\042 %s read1.sai read2.sai %s %s | samtools view -bS - > %s_fastq.bam" % (ref, pair[0], pair[1], name), shell=True)
    call("rm read1.sai read2.sai", shell=True)
    call("samtools sort %s_fastq.bam %s_sort" % (name, name), shell=True)
    call("samtools index align_sort.bam", shell=True)
    call("rm %s_fastq.bam" % (name), shell=True)
    call("samtools flagstat %s_sort.bam > %s_sort.flagstat" % (name, name), shell=True)
    if reduce == "reduce":
        call("reduce_bam.py %s_sort.bam && rm %s_sort.bam" % (name, name), shell=True)
