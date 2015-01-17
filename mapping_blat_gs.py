#!/usr/bin/python

import sys, os
from subprocess import call

print "\nUsage: finding_sequences.py ListOfSequences Reference NumberOfThreads\n"

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


files = open(lista).readlines()

for n in range(0,len(files)/2):
    file1 = files[n*2][:-1]
    file2 = files[(n*2)+1][:-1]

    w = open("tmp.list","w")
    w.write(file1[:-3]+".fa\n")
    w.write(file2[:-3]+".fa\n")
    w.close()
 
    # convert fq.gz to fasta
    call("seqtk seq -a %s > %s" % (file1,file1[:-3]+".fa"),shell=True)
    call("seqtk seq -a %s > %s" % (file2,file2[:-3]+".fa"),shell=True)

    # run blat to find reads
#    call("blat %s %s %s" % (reference,file1[:-3]+".fa",file1[:-3]+".psl"),shell=True)
    call("blat_recursive.py %s %s %s" % (threads, "tmp.list", reference), shell=True)

    # remove fasta and temp list
    call("rm %s" % file1[:-3]+".fa", shell=True)
    call("rm %s" % file2[:-3]+".fa", shell=True)
    call("rm tmp.list", shell=True)

    # join psl
    psl1 = open(file1[:-3]+".fa.blat").readlines()
    psl2 = open(file2[:-3]+".fa.blat").readlines()
    psl_all = open(file1[:-3]+".all.psl", "w")
    psl_all.write("".join(psl1))
    psl_all.write("".join(psl2[5:]))
    psl_all.close()    

    # remove psl
    call("rm %s" % file1[:-3]+".fa.blat", shell=True)
    call("rm %s" % file2[:-3]+".fa.blat", shell=True)

    # get read list
    call("extract_reads_blat.py %s" % file1[:-3]+".all.psl", shell=True)

    # convert GZ to FASTQ and shuffle
    call("seqtk seq -a %s > %s" % (file1, file1+".fq"), shell=True)
    call("seqtk seq -a %s > %s" % (file2, file2+".fq"), shell=True)

    # get reads
    call("seqtk subseq %s %s > %s" % (file1,file1[:-3]+".all.psl.list",file1[:-3]+".sel.fq"), shell=True)
    call("seqtk subseq %s %s > %s" % (file2,file1[:-3]+".all.psl.list",file2[:-3]+".sel.fq"), shell=True)

    # remove FASTQ files
    call("rm %s" % file1+".fq",shell=True)
    call("rm %s" % file2+".fq",shell=True)
    
    # gsMapper
    call("runMapping -ref %s -read %s %s" % (reference, file1[:-3]+".sel.fq", file2[:-3]+".sel.fq"), shell=True)

    # change name
    file_name = file1.split(".")
    file_name = file_name[0]
    ff = os.listdir(".")
    fm = []
    for f in ff:
        if f.endswith("_runMapping"):
            fm.append(f)
    call("mv %s %s" % (fm[-1],file_name+"_mapping"), shell=True)

    # Index bam file
    call("samtools index %s_mapping/454Contigs.bam" % file_name, shell=True) 
