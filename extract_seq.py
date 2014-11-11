#!/usr/bin/python

from Bio import SeqIO
import sys

# open FASTA and list of sequences

try:
	secu = sys.argv[1]
	lis = sys.argv[2]
except:
	secu = raw_input("Sequence FASTA file: ")
	lis = raw_input("List name file: ")

secu = SeqIO.parse(open(secu), "fasta")

lista = [line.strip() for line in open(lis)]

# create lists

names = []
seque = []

# create a dictionary with name and sequence

print "\nCreating database...\n"

for a in secu:
	names.append(a.id)
	seque.append(a.seq)

dictio = dict(zip(names, seque))

# print output

output = open(lis + ".extract", "w")

i = 0
j = 0

for b in lista:
	try:
		output.write(">" + b + "\n")
		output.write(str(dictio[b])+"\n")
		print "Getting sequence %s" % b
		i += 1
	except:
		print "Not found " + b
		j += 1
		pass

print "\nFOUND " + str(i) + " sequences" 
print "\nNOT FOUND " + str(j) + " sequences" 
