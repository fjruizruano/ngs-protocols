#!/usr/bin/python

import sys
import os
from subprocess import call
from Bio import SeqIO

print "Usage: mitobim_run.py NumberOfReads ListOfFiles Reference [miramito/quickmito/seedmito] missmatch"

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

try:
    prot = sys.argv[4]
except:
    prot = raw_input("Introduce protocol name (miramito/quickmito/seedmito): ")

try:
    mism = sys.argv[5]
except:
    mism = "15"

manifest = """echo "\n#manifest file for basic mapping assembly with illumina data using MIRA 4\n\nproject = initial-mapping-testpool-to-Salpinus-mt\n\njob=genome,mapping,accurate\n\nparameters = -NW:mrnl=0 -AS:nop=1 SOLEXA_SETTINGS -CO:msr=no\n\nreadgroup\nis_reference\ndata = reference.fa\nstrain = Salpinus-mt-genome\n\nreadgroup = reads\ndata = reads.fastq\ntechnology = solexa\nstrain = testpool\n" > manifest.conf"""

miramito = """mira manifest.conf && MITObim_1.8.pl --missmatch %s --clean -start 1 -end 1000 -sample testpool -ref Salpinus_mt_genome -readpool reads.fastq -maf initial-mapping-testpool-to-Salpinus-mt_assembly/initial-mapping-testpool-to-Salpinus-mt_d_results/initial-mapping-testpool-to-Salpinus-mt_out.maf > log""" % mism

quickmito = """MITObim_1.8.pl -start 1 -end 1000 -sample testpool -ref Salpinus_mt_genome -readpool reads.fastq --missmatch %s --quick reference.fa --clean > log""" % mism

seedmito = """MITObim_1.8.pl -sample testpool -ref Salpinus_mt_genome -readpool reads.fastq --quick reference.fa --missmatch %s -end 1000 --clean > log""" % mism

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
    name = name[:-2]
    foldername = "%s_%s" % (name,prot)
    call("mkdir %s" % foldername , shell=True)
    os.chdir(foldername)

    print "\nStarting with " + name

    call("seqtk sample -s100 ../%s %s > %s" % (pairone,nreads,name+".fq.subset1"), shell=True)
    call("seqtk sample -s100 ../%s %s > %s" % (pairtwo,nreads,name+".fq.subset2"), shell=True)
    call("shuffleSequences_fastq.pl %s %s %s" % (name+".fq.subset1",name+".fq.subset2",name+".shuffled.fastq"), shell=True)
    call("ln -sf %s reads.fastq" % (name+".shuffled.fastq"), shell=True)
    call("ln -sf ../%s reference.fa" % ref, shell=True)
    if prot == "miramito":
        call(manifest, shell=True)
        call(miramito, shell=True)
    elif prot == "quickmito":
        call(quickmito, shell=True)
    elif prot == "seedmito":
        call(seedmito, shell=True)
    else:
        break
    list_dir = os.listdir(".")
    list_dir.sort()
    iterations = []
    for dir in list_dir:
        if dir.startswith("iteration"):
            iterations.append(dir)
    os.chdir("../")
    consensus = "%s/%s" % (foldername,iterations[-1]+miramitoout)
    secus = SeqIO.parse(open(consensus), "fasta")
    out = open("%s_%s.fa" % (name,prot), "w")
    i = 0
    for secu in secus:
        i+=1
        s = str(secu.seq)
        s = s.replace("x","n")
        out.write(">%s_%s_%s\n%s\n" % (name,prot,i, s))
    out.close()

    print name + " finalized!!!"
