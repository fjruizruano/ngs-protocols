#!/usr/bin/python

import sys
import os
from subprocess import call
from Bio import SeqIO

print "Usage: mitobim_run.py NumberOfReads ListOfFiles Reference"

try:
    nreads = sys.argv[1]
except:
    nreads = raw_input("Introduce number of reads: ")

try:
    lista = sys.argv[2]
except:
    lista = raw_input("Introduce list of files: ")

try:
    ref = sys.argv[3]
except:
    ref = raw_input("Introduce Fasta file as reference: ")

manifest = """echo "\n#manifest file for basic mapping assembly with illumina data using MIRA 4\n\nproject = initial-mapping-testpool-to-Salpinus-mt\n\njob=genome,mapping,accurate\n\nparameters = -NW:mrnl=0 -AS:nop=1 SOLEXA_SETTINGS -CO:msr=no\n\nreadgroup\nis_reference\ndata = reference.fa\nstrain = Salpinus-mt-genome\n\nreadgroup = reads\ndata = reads.fastq\ntechnology = solexa\nstrain = testpool\n" > manifest.conf"""

miramito = """mira manifest.conf && MITObim_1.8.pl --clean -start 1 -end 1000 -sample testpool -ref Salpinus_mt_genome -readpool reads.fastq -maf initial-mapping-testpool-to-Salpinus-mt_assembly/initial-mapping-testpool-to-Salpinus-mt_d_results/initial-mapping-testpool-to-Salpinus-mt_out.maf > log"""

miramitoout = """/testpool-Salpinus_mt_genome_assembly/testpool-Salpinus_mt_genome_d_results/testpool-Salpinus_mt_genome_out_testpool.unpadded.fasta"""

pairs = open(lista).readlines()

npairs = len(pairs)/2

for npair in range(0,npairs):
    pairone = pairs[npair*2][:-1]
    pairtwo = pairs[(npair*2)+1][:-1]
    name = ""
    paironesplit = pairone.split(".")
    if paironesplit[-1] == "gz":
        name = ".".join(paironesplit[0:-2])
    elif paironesplit[-1] == "fastq" or paironesplit[-1] == "fq":
        name = ".".join(paironesplit[0:-1])
    call("mkdir %s" % name , shell=True)
    os.chdir(name)

    call("seqtk sample -s100 ../%s %s > %s" % (pairone,nreads,name+".fq.subset1"), shell=True)
    call("seqtk sample -s100 ../%s %s > %s" % (pairtwo,nreads,name+".fq.subset2"), shell=True)
    call("shuffleSequences_fastq.pl %s %s %s" % (name+".fq.subset1",name+".fq.subset2",name+".shuffled.fastq"), shell=True)
    call("ln -sf %s reads.fastq" % (name+".shuffled.fastq"), shell=True)
    call("ln -sf ../%s reference.fa" % ref, shell=True)
    call(manifest, shell=True)
    call(miramito, shell=True)
    list_dir = os.listdir(".")
    list_dir.sort()
    iterations = []
    for dir in list_dir:
        if dir.startswith("iteration"):
            iterations.append(dir)
    os.chdir("../")
    consensus = "%s/%s" % (name,iterations[-1]+miramitoout)
    secus = SeqIO.parse(open(consensus), "fasta")
    out = open(name+"_consensus.fa", "w")
    for secu in secus:
        s = str(secu.seq)
        s = s.replace("x","n")
        out.write(">%s\n%s\n" % (str(secu.id), s))
    out.close()
