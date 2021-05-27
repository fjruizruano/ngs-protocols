#!/usr/bin/env python

from Bio import SeqIO
import sys
from itertools import combinations
from subprocess import call

try:
    fasta=sys.argv[1]
except:
    fasta=input("Introduce fasta file with the selected reads: ")

# load fasta
data = SeqIO.index(fasta, "fasta")

# create length file
out = open("length.txt", "w")
for s in data:
    out.write("%s %s\n" % (s, str(len(data[s].seq))))
out.close()

# get list of ids in the fasta
seqs=[d for d in data]

# create file
out = open("all_shared_SUNKs.tbl", "w")
out.close()

# get shared kmers
for s in seqs:
    print(s)
    call("""grep "%s" reads.positions > 1.txt""" % s, shell=True)
    call("""grep -v "%s" reads.positions > 2.txt""" % s, shell=True)
    call("SUNKsharing.py -1 1.txt -2 2.txt -l length -o OUT", shell=True)
    call("tail -n +2 OUT >> all_shared_SUNKs.tbl", shell=True)
call("rm 1.txt 2.txt OUT", shell=True)

# get pairwise combination of ids
comb=list(combinations(seqs,2))

# create dictionary
comb_dict = {}

# include id pairs in the dictionary
for el in comb:
    comb_dict[el] = []

# get shared kmers
shared = open("all_shared_SUNKs.tbl").readlines()
for l in shared:
    info = l.split()
    pair = (info[0],info[2])
    kmer = info[5]
    if pair in comb_dict:
        comb_dict[pair].append(kmer)

# write results in a text file
out = open("shared_SUNKs.tbl", "w")
for el in comb:
    out.write("%s\t%s\t%s\t%s\n" % (el[0], el[1], str(len(comb_dict[el])), "\t".join(comb_dict[el])))
out.close()
