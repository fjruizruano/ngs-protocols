#!/usr/bin/python

from Bio import SeqIO

file = raw_input("FASTA file: ")
length = int(raw_input("Length of the sequences: "))

secu = SeqIO.parse(open(file), "fasta")

output = open("output.fas","w")

for s in secu:
	cut_times = len(str(s.seq))/length
	for n in range(0, cut_times+1):
		output.write(">%s_%s\n%s\n" % (s.id, str(n), str(s.seq)[n*length:(n+1)*length]))
