#!/usr/bin/python

import sys, os
from subprocess import call

print "\nUsage: rexp_prepare.py NumberOfPairedReads File_1.fastq File_2.fastq [PREFIX]\n"

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

#prefix
try:
    prefix = sys.argv[4]
except:
    prefix = ""

#list of files in the current directory
files = [f for f in os.listdir(".") if os.path.isfile(f)]

#files names
name = r1.split(".")
name = ".".join(name[:-1])
name = name[:-2]
print "Analyzing %s\n" % name

#Getting paired reads
fastq_combine_pe = "fastq_paired_combine_id.py %s %s" % (r1, r2)

#random selection of reads
fastq_pe_random_1 = "seqtk sample -s 100 %s_paired_1.fastq %s > %s_paired_1.fastq.subset" % (name, sel_reads, name)
fastq_pe_random_2 = "seqtk sample -s 100 %s_paired_2.fastq %s > %s_paired_2.fastq.subset" % (name, sel_reads, name)

#shuffle reads
shuffle = "shuffleSequences_fastq.pl %s %s %s" % (name+"_paired_1.fastq.subset", name+"_paired_2.fastq.subset", name+"_all_"+prefix+str(sel_reads)+".fastq")

#convert fastq to fasta
fastq_to_fasta =  "seqtk seq -a %s > %s" % (name+"_all_"+prefix+str(sel_reads)+".fastq", name+"_all_"+prefix+str(sel_reads)+".fasta")

if name+"_paired_2.fastq" not in files or name+"_paired_1.fastq" not in files:
    try:
        print "Running Fastq-combine-pe"
        print fastq_combine_pe
        call(fastq_combine_pe,shell=True)
    except:
        print "Fastq-combine-pe could not run. Try again.\n"
else:
    print "Fastq-combine-pe was already run. Skipping.\n"

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
fqtemp = open("%s_all_%s%s_temp.fastq" % (name,prefix,str(sel_reads)) ,"w")

#read modified fasta file
print "Editing "+ name+"_all_"+prefix+str(sel_reads)+".fastq\n"
fastq = open(name+"_all_"+prefix+str(sel_reads)+".fastq").readlines()

#add prefix
for x in range(0,len(fastq)):
    if x%8 == 0:
        line = fastq[x]
        line = ">%s%s%s" % (prefix,line[:-2],"1\n")
    elif x%8 == 4:
        line = fastq[x]
        line = ">%s%s%s" % (prefix,line[:-2],"2\n")
    else:
        line = fastq[x]
    fqtemp.write(line)

fqtemp.close()

call("mv %s %s" % (name+"_all_"+prefix+str(sel_reads)+"_temp.fastq", name+"_all_"+prefix+str(sel_reads)+".fastq"), shell=True)

#Try to convert to fasta format
try:
    print "Running Fastq to fasta"
    print fastq_to_fasta
    call(fastq_to_fasta, shell = True)
except:
    print "Fastq to fasta could not run. Try again.\n"

print "\nWe\'re done!\n"
