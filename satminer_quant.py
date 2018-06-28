#!/usr/bin/python

import sys
import operator
from subprocess import call
from Bio import SeqIO

print "Usage: satminer_quant.py SamplesFile FastaFileMonomers"

try:
    sam_file = sys.argv[1]
except:
    sam_file = raw_input("Introduce Samples File: ")

try:
    fasta_file = sys.argv[2]
except:
    fasta_file = raw_input("Introduce FASTA file with monomers: ")

print "Loading files.\n"

#loading samples file
##loading reference sample and repeat landscapes
samples = open(sam_file).readlines()
samples_rl = samples[0][:-1]
samples_rl = samples_rl.split("\t")
sp_name = samples_rl[0]
ref_library = samples_rl[1]
rep_land = samples_rl[2]

##loading divsum files
lib_dict = {}
for lib in samples[1:]:
    lib = lib[:-1]
    lib = lib.split("\t")
    lib_dict[lib[0]] = lib[1:]

##loading divsum file
ref_divsum = lib_dict[ref_library][0]

print ref_library+" is the reference library.\n"
print "Defining families.\n"

call("divsum_ab.py %s %s" % (ref_divsum, fasta_file), shell=True) # CORREGIR

print "Generating divsum file per families"

for line in samples[1:]:
    line = line.split()
    divsum = line[1]
    align = divsum.replace(".divsum", ".align")
    call("sat_subfam2fam.py %s %s" % (align, "pattern.txt" ), shell=True)

call("divsum_to_rl.py %s" % sam_file, shell=True)

call("replace_patterns.py %s %s" % ("table.txt", "equivalences.txt"), shell=True)
call("replace_patterns.py %s %s" % (fasta_file+".abc", "equivalences.txt"), shell=True)
call("replace_patterns.py %s %s" % (fasta_file+".dim.abc", "equivalences.txt"), shell=True)
