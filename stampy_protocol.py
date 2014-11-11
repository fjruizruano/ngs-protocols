#!/usr/bin/python

from subprocess import call

ref = raw_input("FASTA reference file: ")
lib1 = raw_input("FASTQ read library 1 file 1: ")
lib2 = raw_input("FASTQ read library 2 file 1: ")
threads = raw_input("number of threads: ")

try:
	open(ref+".pac")
	open(ref+".ann")
	open(ref+".amb")
	open(ref+".bwt")
	open(ref+".sa")
except:
	call("bwa index -a bwtsw %s" % ref, shell=True)
	call("stampy.py --species=lmig --assembly=1 -G lmig1 %s" % ref, shell=True)
	call("stampy.py -g lmig1 -H lmig1")

call("bwa aln -t%s %s %s > read1.sai" % (threads, ref, lib1), shell=True)

call("bwa aln -t%s %s %s > read2.sai" % (threads, ref, lib2), shell=True)

call("bwa sampe -s -r \042@RG\tID:1\tLB:1\tSM:1\042 %s read1.sai read2.sai %s %s | samtools view -bS - > align_fastq.bam" % (ref, lib1, lib2), shell=True)

call("stampy.py -g lmig1 -h lmig1 -t %s --substitutionrate=0.10 --bamkeepgoodreads -M align_fastq.bam > mapping.sam" % threads, shell=True)

#call("samtools sort align_fastq.bam align_sort", shell=True)

#call("samtools index align_sort.bam", shell=True)

#call("samtools flagstat align_sort.bam > align_sort.flagstat", shell=True)
