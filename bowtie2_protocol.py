#!/usr/bin/python

import sys
from subprocess import call

print "\nUsage: bowtie2_protocol.py ListOfReads Reference Threads [noreduce/reduce]\n"

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

ref_pref = ref.split(".")
ref_pref = ref_pref[:-1]
ref_pref = ".".join(ref_pref)

try:
	open(ref_pref+".1.bt2")
	open(ref_pref+".2.bt2")
	open(ref_pref+".3.bt2")
	open(ref_pref+".4.bt2")
	open(ref_pref+".rev.1.bt2")
	open(ref_pref+".rev.2.bt2")
except:
	call("bowtie2-build %s %s" % (ref, ref_pref), shell=True)

for pair in l_files:
    name = pair[0]
    name = name.split(".")
    name = name[0][:-2]
    call("bowtie2 --very-sensitive -p %s -x %s -1 %s -2 %s | samtools view -bS -> %s_fastq.bam" % (threads, ref_pref, pair[0], pair[1], name), shell=True)
    call("samtools sort -T aln.sorted %s_fastq.bam -o %s_sort.bam" % (name, name), shell=True)
    call("samtools index %s_sort.bam" % (name), shell=True)
    call("rm %s_fastq.bam" % (name), shell=True)
    call("samtools flagstat %s_sort.bam > %s_sort.flagstat" % (name, name), shell=True)
    if reduce == "reduce":
        call("reduce_bam.py %s_sort.bam && rm %s_sort.bam" % (name, name), shell=True)
        call("rm %s_sort.bam.bai" % (name), shell=True)
