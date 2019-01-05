#!/usr/bin/python

import sys
from subprocess import call

print "\nUsage: extract_barcoded_reads_from_bam.py BamFile BarcodedFastqFile\n"

try:
    bam_file = sys.argv[1]
except:
    bam_file = raw_input("Introduce BAM file with mapped reads to select: ")

try:
    bc_file = sys.argv[2]
except:
    bc_file = raw_input("Introduce Barcoded FASTQ file from 10XG Longranger: ")

bc_question = ""
if bc_file.endswith(".fastq") or bc_file.endswith(".fq"):
    bc_question = "fastq"
elif bc_file.endswith(".fastq.gz") or bc_file.endswith(".fq.gz"):
    bc_question = "gz"
else:
    sys.exit("\nERROR. Please, review barcoded file.\n")

bam_to_fastq = """samtools view %s | cut -f1,10,11 | sed 's/^/@/' | sed 's/\134t/\134n/' | sed 's/\134t/\134n+\134n/' > mapped_reads.fastq""" % (bam_file)

print bam_to_fastq
call(bam_to_fastq, shell=True)

fastq_to_names = """grep "@ST-E00" mapped_reads.fastq | sort | uniq | sed 's/@//g' > mapped_reads_names.txt"""

print fastq_to_names
call(fastq_to_names, shell=True)

names_to_fastq = """seqtk subseq %s mapped_reads_names.txt > mapped_reads_names.fastq""" % (bc_file)

print names_to_fastq
call(names_to_fastq, shell=True)

fastq_to_bc = """grep "BX:Z:" mapped_reads_names.fastq | awk {'print $2'} | sort | uniq > mapped_reads_barcodes.txt"""

print fastq_to_bc
call(fastq_to_bc, shell=True)

bc_to_bcnames = ""
if bc_question == "fastq":
    bc_to_bcnames = "grep -f mapped_reads_barcodes.txt %s > barcodes_names.txt" % (bc_file)
elif bc_question == "gz":
    bc_to_bcnames = "zgrep -f mapped_reads_barcodes.txt %s > barcodes_names.txt" % (bc_file)

print bc_to_bcnames
call(bc_to_bcnames, shell=True)

bcnames_to_bcreads = """awk {'print $1'} barcodes_names.txt | sed 's/@//g' | sort | uniq > barcodes_reads.txt"""

print bcnames_to_bcreads
call(bcnames_to_bcreads, shell=True)

bcreads_to_reads = """seqtk subseq %s barcodes_reads.txt > barcodes_reads.fastq""" % (bc_file)

print bcreads_to_reads
call(bcreads_to_reads, shell=True)
