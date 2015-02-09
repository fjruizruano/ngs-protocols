#!/usr/bin/python

import sys, os
from subprocess import call
from commands import getstatusoutput
from os import listdir
from os.path import isfile, join

print "\nUsage: mapping_blat_gs.py ListOfSequences Reference NumberOfThreads [map/div/mapdiv/nomap]\n"

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
#    call("seqtk seq -a %s > %s" % (file1, file1+".fq"), shell=True)
#    call("seqtk seq -a %s > %s" % (file2, file2+".fq"), shell=True)

    # get reads
    call("seqtk subseq %s %s > %s" % (file1,file1[:-3]+".all.psl.list",file1[:-3]+".sel.fq"), shell=True)
    call("seqtk subseq %s %s > %s" % (file2,file1[:-3]+".all.psl.list",file2[:-3]+".sel.fq"), shell=True)

    # remove FASTQ files
#    call("rm %s" % file1+".fq",shell=True)
#    call("rm %s" % file2+".fq",shell=True)
    
    #RepeatMasker and Abundance/Divergence analysis
    if map_question == "div" or map_question == "mapdiv":
        call("seqtk seq -a %s > %s" % (file1[:-3]+".sel.fq", file1[:-3]+".sel.fa"), shell=True)
        call("seqtk seq -a %s > %s" % (file2[:-3]+".sel.fq", file2[:-3]+".sel.fa"), shell=True)
        call("shuffleSequences_fasta.pl %s %s %s" % (file1[:-3]+".sel.fa", file2[:-3]+".sel.fa", file1[:-3]+".all.fa"), shell=True)
        n_nucs = getstatusoutput("""grep -v ">" %s | wc | awk '{print $3-$1}'""" % (file1[:-3]+".all.fa"))
        n_nucs = int(n_nucs[1])
        n_division = n_nucs/10**8
        if n_division > 0:
            call("faSplit sequence %s %s %s" % (file1[:-3]+".all.fa",str(n_division+1),file1[:-3]+".split.."), shell=True)
            onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
            splits = []
            for f in onlyfiles:
                if f.startswith(file1[:-3]+".split.") and f.endswith(".fa"):
                    splits.append(f)
            splits.sort()
            for n in range(0,len(splits)):
                call("RepeatMasker -pa %s -a -nolow -no_is -lib %s %s" % (threads, reference, splits[n]), shell=True)
                call("cat %s >> %s" % (splits[n]+".align",file1[:-3]+".all.fa.align"), shell=True)
        elif n_division == 0:
            call("RepeatMasker -pa %s -a -nolow -no_is -lib %s %s" % (threads, reference, file1[:-3]+".all.fa"), shell=True)
        call("calcDivergenceFromAlign.pl -s %s %s" % (file1[:-3]+".all.fa.align.divsum", file1[:-3]+".all.fa.align"), shell=True)

    # gsMapper
    if map_question == "map" or map_question == "mapdiv":
        call("runMapping -cpu %s -ref %s -read %s %s" % (threads, reference, file1[:-3]+".sel.fq", file2[:-3]+".sel.fq"), shell=True)

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

    #Nothing more happens
    if map_question == "nomap":
        pass
