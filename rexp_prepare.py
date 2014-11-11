#!/usr/bin/python

import sys
from subprocess import call

try:
    sel_reads = sys.argv[1]
    sel_reads = int(sel_reads)
except:
    sel_reads = raw_input("Number of reads you want select: ")
    sel_reads = int(sel_reads)

try:
    r1 = sys.argv[2]
    r2 = sys.argv[3]
except:
    r1 = raw_input("FASTQ file 1: ")
    r2 = raw_input("FASTQ file 2: ")

try:
    prefix = sys.argv[4]
except:
    prefix = ""

rr1 = r1.find(".")
suffix = r1[rr1:]
rr1 = r1[:rr1]
rrr1 = r1.find("_")
rrr1 = r1[:rrr1]
rr2 = r2.find(".")
rr2 = r2[:rr2]

with open(r1) as myfile:
    head = [next(myfile) for x in xrange(2)]
len_reads = str(len(head[1])-1)

trimmomatic = "trimmomatic PE -phred33 %s %s %s %s %s %s ILLUMINACLIP:/usr/local/lib/Trimmomatic-0.32/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:30 MINLEN:%s" % (r1, r2, rr1+"_paired"+suffix, rr1+"_unpaired"+suffix, rr2+"_paired"+suffix, rr2+"_unpaired"+suffix, len_reads)

fastq_pe_random = "fastq-pe-random.py %s %s %s" % (rr1+"_paired"+suffix, rr2+"_paired"+suffix, sel_reads)

shuffle = "shuffleSequences_fastq.pl %s %s %s" % (rr1+"_paired"+suffix+".subset", rr2+"_paired"+suffix+".subset", rrr1+"_all.fastq")

fastq_to_fasta = """awk 'BEGIN{P=1}{if(P==1||P==2){gsub(/^[@]/,">");print}; if(P==4)P=0; P++}' %s > %s""" % (rrr1+"_all.fastq", rrr1+"_all.fasta")

try:
    print "Running Trimmomatic"
    call(trimmomatic, shell = True)
except:
    print "Trimmomatic could not run. Try again."

try:
    print "Running Fastq-pe-random"
    call(fastq_pe_random, shell = True)
except:
    print "Fastq-pe-random could not run. Try again."

try:
    print "Running Shuffling"
    call(shuffle, shell = True)
except:
    print "Shffling could not run. Try again."

try:
    print "Running Fastq to fasta"
    print fastq_to_fasta
    call(fastq_to_fasta, shell = True)
except:
    print "Fastq to fasta could not run. Try again"

ready = open(rrr1+"_all_ready.fasta","w")
fasta = open(rrr1+"_all.fasta").readlines()
for x in range(0,len(fasta)):
    if x%4 == 0:
        line = fasta[x]
        line = line.split(" ")
        line = ">%s%s%s" % (prefix,line[0][1:],"/1\n")
    elif x%4 == 2:
        line = fasta[x]
        line = line.split(" ")
        line = ">%s%s%s" % (prefix,line[0][1:],"/2\n")
    else:
        line = fasta[x]
    ready.write(line)
