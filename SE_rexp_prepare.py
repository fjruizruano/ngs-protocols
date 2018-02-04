#!/usr/bin/python

import sys, os
from subprocess import call

print "\nUsage: SE_rexp_prepare.py NumberOfPairedReads File.fastq MinQual MinLen [PREFIX]\n"

##read parameters
#number of reads
try:
    sel_reads = sys.argv[1]
    sel_reads = int(sel_reads)
except:
    sel_reads = raw_input("Number of reads you want select: ")
    sel_reads = int(sel_reads)

#FASTQ files
try:
    r1 = sys.argv[2]
except:
    r1 = raw_input("FASTQ file 1: ")

try:
    mq = sys.argv[3]
    ml = sys.argv[4]
except:
    ml = 101
    mq = 30

#prefix
try:
    prefix = sys.argv[5]
except:
    prefix = ""

#list of files in the current directory
files = [f for f in os.listdir(".") if os.path.isfile(f)]

#files names
rr1 = r1.find(".")
suffix = r1[rr1:]
rr1 = r1[:rr1]
#rrr1 = r1.find("_")
#rrr1 = r1[:rrr1]

print rr1

#with open(r1) as myfile:
#    head = [next(myfile) for x in xrange(2)]
#len_reads = str(len(head[1])-1)

#Trimming with Trimmomatic
trimmomatic = "trimmomatic SE -phred33 %s %s ILLUMINACLIP:/usr/local/lib/Trimmomatic-0.32/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:%s MINLEN:%s" % (r1, rr1+"_trimmed.fastq", mq, ml)

print trimmomatic

#random selection of reads

fastq_random_1 = "seqtk sample -s 100 %s %s > %s" % (rr1+"_trimmed.fastq",sel_reads,rr1+"_trimmed.fastq.subset")

#convert fastq to fasta
fastq_to_fasta =  "seqtk seq -a %s > %s" % (rr1+"_trimmed.fastq.subset",rr1+"_all_"+prefix+str(sel_reads)+".fasta")

#Try to run Trimmomatic

if rr1+"_trimmed.fastq" not in files:
    try:
        print "Running Trimmomatic\n"
        print trimmomatic
        call(trimmomatic, shell = True)
    except:
        print "Trimmomatic could not run. Try again.\n"
else:
    print "Trimmomatic was already run. Skipping.\n"

#Try to run fastq pe random
try:
    print "Running Fastq-random"
    print fastq_random_1
    call(fastq_random_1, shell = True)
except:
    print "Fastq-random could not run. Try again.\n"

#Try to convert to fasta format
try:
    print "Running Fastq to fasta"
    print fastq_to_fasta
    call(fastq_to_fasta, shell = True)
except:
    print "Fastq to fasta could not run. Try again.\n"

#open output
fatemp = open("%s_all_%s%s_temp.fasta" % (rr1,prefix,str(sel_reads)) ,"w")

#read modified fasta file
print "Editing "+ rr1+"_all_"+prefix+str(sel_reads)+".fastq\n"
fasta = open(rr1+"_all_"+prefix+str(sel_reads)+".fasta").readlines()

#add prefix
for x in range(0,len(fasta)):
    if x%2 == 0:
        line = fasta[x]
        line = line.split(">")
        line = ">%s%s" % (prefix,line[1])
    else:
        line = fasta[x]
    fatemp.write(line)

fatemp.close()

call("mv %s %s" % (rr1+"_all_"+prefix+str(sel_reads)+"_temp.fasta",rr1+"_all_"+prefix+str(sel_reads)+".fasta"), shell=True)

print "\nWe\'re done!\n"
