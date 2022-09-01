#!/usr/bin/python

from Bio import SeqIO
import sys

print "get_coordinates file.fasta"

# open FASTA and list of sequences

try:
	secu = sys.argv[1]
except:
	secu = raw_input("Sequence FASTA file: ")

s = SeqIO.parse(open(secu), "fasta")

name = secu.split(".")
name = name[:-1]
name = ".".join(name)
name = name+".coordinates.txt"

output = open(name, "w")

for a in s:
	n = a.id
	l = len(a.seq)
	output.write("%s\t%s\t\t\t\n" % (n,str(l)))

output.close()
