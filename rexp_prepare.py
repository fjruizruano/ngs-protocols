#!/usr/bin/python

import sys, os
from subprocess import call

print "\nUsage: rexp_prepare.py NumberOfPairedReads File_1.fastq File_2.fastq MinQual MinLen [PREFIX]\n"

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
    r2 = sys.argv[3]
except:
    r1 = raw_input("FASTQ file 1: ")
    r2 = raw_input("FASTQ file 2: ")

#Trimming
try:
    mq = sys.argv[4]
    ml = sys.argv[5]
except:
    ml = 101
    mq = 30

#prefix
try:
    prefix = sys.argv[6]
except:
    prefix = ""

#list of files in the current directory
files = [f for f in os.listdir(".") if os.path.isfile(f)]

#files names
rr1 = r1.find(".")
suffix = r1[rr1:]
rr1 = r1[:rr1]
rrr1 = r1.find("_")
rrr1 = r1[:rrr1]
rr2 = r2.find(".")
rr2 = r2[:rr2]

print rrr1

#with open(r1) as myfile:
#    head = [next(myfile) for x in xrange(2)]
#len_reads = str(len(head[1])-1)

#Trimming with Trimmomatic
trimmomatic = "trimmomatic PE -phred33 %s %s %s %s %s %s ILLUMINACLIP:/usr/local/lib/Trimmomatic-0.32/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:%s MINLEN:%s" % (r1, r2, rr1+"_paired.fastq", rr1+"_unpaired.fastq", rr2+"_paired.fastq", rr2+"_unpaired.fastq", mq, ml)

#random selection of reads

fastq_pe_random_1 = "seqtk sample -s 100 %s %s > %s" % (rr1+"_paired.fastq",sel_reads,rr1+"_paired.fastq.subset")
fastq_pe_random_2 = "seqtk sample -s 100 %s %s > %s" % (rr2+"_paired.fastq",sel_reads,rr2+"_paired.fastq.subset")

#fastq_pe_random = "fastq-pe-random.py %s %s %s" % (rr1+"_paired"+suffix, rr2+"_paired"+suffix, sel_reads)

#shuffle reads
shuffle = "shuffleSequences_fastq.pl %s %s %s" % (rr1+"_paired.fastq.subset", rr2+"_paired.fastq.subset", rrr1+"_all_"+prefix+str(sel_reads)+".fastq")

#convert fastq to fasta
fastq_to_fasta =  "seqtk seq -a %s > %s" % (rrr1+"_all_"+prefix+str(sel_reads)+".fastq",rrr1+"_all_"+prefix+str(sel_reads)+".fasta")

#Try to run Trimmomatic

if rr1+"_paired.fastq" not in files or rr2+"_paired.fastq" not in files:
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
    print "Running Fastq-pe-random"
    print fastq_pe_random_1
    call(fastq_pe_random_1, shell = True)
    print fastq_pe_random_2
    call(fastq_pe_random_2, shell = True)
except:
    print "Fastq-pe-random could not run. Try again.\n"

#Try to run shuffling
try:
    print "\nRunning Shuffling"
    print shuffle+"\n"
    call(shuffle, shell = True)
except:
    print "Shuffling could not run. Try again.\n"

#open output
fqtemp = open("%s_all_%s%s_temp.fastq" % (rrr1,prefix,str(sel_reads)) ,"w")

#read modified fasta file
print "Editing "+ rrr1+"_all_"+prefix+str(sel_reads)+".fastq\n"
fastq = open(rrr1+"_all_"+prefix+str(sel_reads)+".fastq").readlines()

#add prefix
for x in range(0,len(fastq)):
    if x%8 == 0:
        line = fastq[x]
        line = line.split(" ")
        line = ">%s%s%s" % (prefix,line[0][1:],"/1\n")
    elif x%8 == 4:
        line = fastq[x]
        line = line.split(" ")
        line = ">%s%s%s" % (prefix,line[0][1:],"/2\n")
    else:
        line = fastq[x]
    fqtemp.write(line)

fqtemp.close()

call("mv %s %s" % (rrr1+"_all_"+prefix+str(sel_reads)+"_temp.fastq",rrr1+"_all_"+prefix+str(sel_reads)+".fastq"), shell=True)

#Try to convert to fasta format
try:
    print "Running Fastq to fasta"
    print fastq_to_fasta
    call(fastq_to_fasta, shell = True)
except:
    print "Fastq to fasta could not run. Try again.\n"

print "\nWe\'re done!\n"
