#!/usr/bin/python

from Bio import SeqIO
import operator
import sys

try:
    secuen_name = sys.argv[1]
    secuen = SeqIO.parse(open(secuen_name), "fasta")
except:
    secuen_name = raw_input("Introduce fasta file: ")
    secuen = SeqIO.parse(open(secuen_name), "fasta")

try:
    len_cutoff = sys.argv[2]
except:
    len_cutoff = raw_input("Introduce length cutoff (integer): ")

len_cutoff = int(len_cutoff)

try:
    sort = "n"
    if sys.argv[3] == "sort":
        sort = "y"
except:
    sort = raw_input("Do you want to sort by length? (y/n): ")

dict_seq = {}
out = open(secuen_name+"."+str(len_cutoff), "w")

for secu in secuen:
    dict_seq[secu.id] = [len(str(secu.seq)),str(secu.seq)]

if sort == "y":
    dict_seq = sorted(dict_seq.iteritems(), key=operator.itemgetter(1))
    for el in range(len(dict_seq)-1,-1,-1):
	if dict_seq[el][1][0] >= len_cutoff:
            out.write(">%s\n%s\n" % (dict_seq[el][0], dict_seq[el][1][1]))
        
else:
    for el in dict_seq:
	if dict_seq[el][0] >= len_cutoff:
            out.write(">%s\n%s\n" % (el,dict_seq[el][1]))

out.close()
