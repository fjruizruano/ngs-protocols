#!/usr/bin/python

import sys
from subprocess import call
from Bio import SeqIO
from Bio import AlignIO

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
cutdict = {}
for gene in genelist:
    gene = gene.split()
    genedict[gene[0]] = []
    if len(gene) > 1:
        cutdict[gene[0]]=gene[1]

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
        abbrev = s[0] 
        abbrev = abbrev.split("_")
        abbrev = abbrev[-1]
        secu = s[1]
        nnum = secu.count("N")
        nprop = 1.0*nnum/len(secu)
        if nprop < 0.2:
            out.write(">%s\n%s\n" % (abbrev, secu))
    out.close()
    call("mafft %s.fasta > %s_ali.fasta" % (el, el) , shell=True)
    if el in cutdict:
        ali = AlignIO.read(open("%s_ali.fasta" % el), "fasta")
        cutinfo = cutdict[el]
        cutparts = cutinfo.split(",")
        for part in cutparts:
            partinfo = part.split("-")
            beg = int(partinfo[0])
            end = int(partinfo[1])
        AlignIO.write(ali[:,beg:end],open("%s_ali_sel.fasta" % el,"w"), "fasta")
        call("./massive_phylogeny_raxml_support.py %s_ali_sel.fasta 100 100 12 %s" % (el, el), shell=True)
    else:
        call("./massive_phylogeny_raxml_support.py %s_ali.fasta 100 100 12 %s" % (el, el), shell=True)
