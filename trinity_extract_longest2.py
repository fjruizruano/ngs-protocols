#!/usr/bin/python

from Bio import SeqIO
import sys
import operator

try:
    secu = sys.argv[1]
except:
    secu = raw_input("Introduce Trinity's output: ")

di = {}

dat = SeqIO.parse(open(secu), "fasta")

for s in dat:
    #extract gene names	
    gene = s.id
    gene = gene.split("_")
    gene = "_".join(gene[:-1])
    #for each gene add isoforms and length
    if gene not in di:
        di[gene] = {s.id:len(s.seq)}
    else:
        di[gene][s.id] = len(s.seq)

#selecting longest isoforms
li = []

for x in di:
    dictio = sorted(di[x].iteritems(),key=operator.itemgetter(1))
    dictio.reverse()
    li.append(dictio[0][0])

#write output
w = open("Trinity.longest.fasta", "w")

dat = SeqIO.parse(open(secu), "fasta")

for s in dat:                                   
    if s.id in li:
        w.write(">%s\n%s\n" % (s.description,s.seq))

w.close()

