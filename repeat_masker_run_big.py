#!/usr/bin/python

import sys, os
from subprocess import call
from commands import getstatusoutput
from os import listdir
from os.path import isfile, join

print "\nUsage: repeat_masker_run_big.py ListOfSequences Reference NumberOfThreads\n"

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

for file in files:
    file = file[:-1]

    n_nucs = getstatusoutput("""grep -v ">" %s | wc | awk '{print $3-$1}'""" % (file))
    n_nucs = int(n_nucs[1])
    n_division = n_nucs/10**8
    if n_division > 0:
        call("faSplit sequence %s %s %s" % (file,str(n_division+1),file+".split.."), shell=True)
        onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
        splits = []
        for f in onlyfiles:
            if f.startswith(file+".split.") and f.endswith(".fa"):
                splits.append(f)
        splits.sort()
        for n in range(0,len(splits)):
            call("RepeatMasker -pa %s -a -nolow -no_is -lib %s %s" % (threads, reference, splits[n]), shell=True)
            call("cat %s >> %s" % (splits[n]+".align",file+".align"), shell=True)
    elif n_division == 0:
        call("RepeatMasker -pa %s -a -nolow -no_is -lib %s %s" % (threads, reference, file), shell=True)
    call("calcDivergenceFromAlign.pl -s %s %s" % (file+".align.divsum", file+".align"), shell=True)

