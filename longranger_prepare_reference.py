#!/usr/bin/python

import sys
from subprocess import call

print "Usage: longranger_prepare_reference.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file: ")

name = file.split(".")
name = ".".join(name[:-1])

extract = "perl /home/fruano/bin/extractSeqFromFasta.pl"

call("sizeseq -sequences %s -descending -outseq %s_sort.fas" % (file, name), shell=True)

call("""grep ">" %s_sort.fas | head -n 999 > %s_999names.txt""" % (name, name), shell=True)

call(extract + " %s_sort.fas list %s_999names.txt > %s_999.fas" % (name, name, name), shell=True)

call("""grep ">" %s_sort.fas | tail -n +1000 > %s_1000names.txt""" % (name, name), shell=True)

call(extract + " %s_sort.fas list %s_1000names.txt > %s_1000.fas" % (name, name, name), shell=True)

Ns = 500*"N"

call("""echo '>remaining\n' > %s_1000join.fas""" % (name), shell=True)
call("cat %s_1000.fas | sed 's/>.*/%s/' | tr -d '\n' >> %s_1000join.fas" % (name, Ns, name), shell=True)
call("cat %s_999.fas %s_1000join.fas > %s_final.fasta" % (name, name, name), shell=True)

