#!/usr/bin/python

from Bio import SeqIO
import sys

print "extract_seq_regions.py FastaFile RegionsFile"

# open FASTA and list of sequences

try:
	secu = sys.argv[1]
	lis = sys.argv[2]
except:
	secu = raw_input("Sequence FASTA file: ")
	lis = raw_input("Regions name_file (sequence_id\tbegin-end): ")

secu = SeqIO.parse(open(secu), "fasta")

lista = [line.strip() for line in open(lis)]

print lista

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

output = open(lis + ".regions", "w")

i = 0
j = 0

for bb in lista:
	bb = bb.split("\t")
	b = bb[0]
        regions = bb[1]
        regions = regions.split("-")
        begin = int(regions[0])-1
        end = int(regions[1])
    	try:
		output.write(">" + b + "\n")
		output.write(str(dictio[b][begin:end])+"\n")
		print "Getting sequence %s" % b
		i += 1
	except:
		print "Not found " + b
		j += 1
		pass

print "\nFOUND " + str(i) + " sequences" 
print "\nNOT FOUND " + str(j) + " sequences" 
