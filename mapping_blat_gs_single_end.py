#!/usr/bin/python

import sys, os
from subprocess import call
from commands import getstatusoutput
from os import listdir
from os.path import isfile, join

print "\nUsage: mapping_blat_gs.py ListOfSequences Reference NumberOfThreads [map/div/mapdiv/ssaha2/ssaha2div/nomap]\n"

try:
    lista = sys.argv[1]
except:
    lista = raw_input("Introduce list of fastq.gz files: ")

try:
    reference = sys.argv[2]
except:
    reference = raw_input("Introduce FASTA file with the refence: ")

try:
    threads = sys.argv[3]
except:
    threads = raw_input("Intruduce number of threads: ")

try:
    map_question = sys.argv[4]
except:
    pass

files = open(lista).readlines()

for n in range(0,len(files)):
    file1 = files[n][:-1]

    w = open("tmp.list","w")
    w.write(file1[:-3]+".fa\n")
    w.close()
 
    # convert fq.gz to fasta
    call("seqtk seq -a %s > %s" % (file1,file1[:-3]+".fa"),shell=True)

    # run blat to find reads
    call("blat_recursive.py %s %s %s" % (threads, "tmp.list", reference), shell=True)

    # remove fasta and temp list
    call("rm %s" % file1[:-3]+".fa", shell=True)
    call("rm tmp.list", shell=True)

    #get unique reads
    call("awk {\047print $10\047} %s | uniq > %s" % (file1[:-3]+".fa.blat", file1[:-3]+".all.psl.list"), shell=True)

    # remove psl
    call("rm %s" % file1[:-3]+".fa.blat", shell=True)

    # get read list
#    reads_file = open("uniq_all.txt").readlines()
#    trimmed_reads = open("uniq_trimmed.txt" ,"w")
#    for read in reads_file:
#        try:
#            read = read[:-3]
#            trimmed_reads.write(read+"\n")
#        except:
#            pass
#    trimmed_reads.close()

#    call("sort %s | uniq > uniq_uniq.txt " %  "uniq_trimmed.txt", shell=True)
#    w = open(file1[:-3]+".all.psl.list","w")
#    uu = open("uniq_uniq.txt").readlines()
#    for l in uu:
#        w.write("%s\n%s\n" % (l[:-1]+"/1",l[:-1]+"/2"))
#    w.close()

    # remove uniq files
#    call("rm uniq_1.txt uniq_2.txt uniq_all.txt uniq_trimmed.txt uniq_uniq.txt", shell=True)

    # get reads
    call("seqtk subseq %s %s > %s" % (file1,file1[:-3]+".all.psl.list",file1[:-3]+".sel.fq"), shell=True)

    #remove list
    call("rm %s" % (file1[:-3]+".all.psl.list"), shell=True)

    # remove FASTQ files
#    call("rm %s" % file1+".fq",shell=True)
#    call("rm %s" % file2+".fq",shell=True)

    # SSAHA2
    if map_question == "ssaha2" or map_question == "ssaha2div":
        call("ls %s > ssaha2_list.txt" % (file1[:-3]+".sel.fq"), shell=True)
        call("ssaha2_run_multi_se.py ssaha2_list.txt %s %s" % (reference,threads), shell=True)
        call("rm ssaha2_list.txt", shell=True)
#        if map_question == "ssaha2div":
#            file1_s = file1.split(".")
#            call("divnuc_bam.py %s %s" % (reference, file1_s[0]+"_mapped.bam"), shell=True)

    #Nothing more happens
    if map_question == "nomap":
        pass
