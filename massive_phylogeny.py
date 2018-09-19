#!/usr/bin/python

import sys
from subprocess import call
from Bio import SeqIO

print "massive_phylo.py FastaFile GeneList"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input("Introduce FASTA file: ")

try:
    genefile = sys.argv[2]
except:
    genefile = raw_input("Introduce Gene list: ")

genelist = open(genefile).readlines()
genedict = {}
for gene in genelist:
    genedict[gene[:-1]] = []

secus = SeqIO.parse(open(fasta), "fasta")
for secu in secus:
    name = str(secu.id)
    prefix = name.split("_")
    prefix = prefix[0]
    secuen = str(secu.seq)
    genedict[prefix].append([name,secuen])

for el in genedict:
    out = open(el+".fasta", "w")
    for s in genedict[el]:
        out.write(">%s\n%s\n" % (s[0], s[1]))
    out.close()
    call("mafft %s.fasta > %s_ali.fasta" % (el, el) , shell=True)
    call("massive_phylogeny_raxml_support.py %s_ali.fasta 100 100 12 %s" % (el, el), shell=True)
