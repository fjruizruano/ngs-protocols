#!/usr/bin/python

from Bio import SeqIO

input = raw_input("Introduce FASTA file: ")

secu = SeqIO.parse(input, "fasta")

output = open(input+".gff", "w")

for sq in secu:
	output.write("%s\tprotein_coding\texon\t1\t%s\t.\t+\t.\tgene_id \042%s\042\n" % (sq.id, str(len(sq.seq)), sq.id))

output.close()

