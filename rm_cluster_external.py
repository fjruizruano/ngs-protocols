#!/usr/bin/python

import sys
from subprocess import call
import os
from os import listdir
from Bio import SeqIO

print "rm_cluster_external.py RepeatMaskerOutFile FastaFile PatternFile"

try:
    outfile = sys.argv[1]
except:
    outfile = raw_input("Introduce RepeatMakser OUT file: ")

try:
    fastafile = sys.argv[2]
except:
    fastafile = raw_input("Introduce FASTA file with the reads: ")

try:
    patfile = sys.argv[3]
except:
    patfile = raw_input("Introduce Pattern File: ")

seq_list = {}
pattern = open(patfile).readlines()
for line in pattern:
    seq = line.split()
    seq = seq[1]
    if seq not in seq_list:
        seq_list[seq] = []

data = open(outfile).readlines()
noheader = data[3:]

for n in range(0, len(noheader)):
    info = noheader[n]
    info = info.split()
    this_line = [info[4],info[9]]
    pair_line = []
    if this_line[0][-1] == "1":
        read = info[4][:-1] + "2"
        pair_line = [read,info[9]]
    elif this_line[0][-1] == "2":
        read = info[4][:-1] + "1"
        pair_line = [read,info[9]]
    sub = noheader[n-3:n] + noheader[n+1:n+4]
    up_down = []
    for el in sub:
        sub_info = el.split()
        up_down.append([sub_info[4],sub_info[9]])
    if pair_line not in up_down:
        seq_list[this_line[1]].append(pair_line[0])
#        print this_line



call("mkdir sel_reads", shell=True)
os.chdir("sel_reads")

sum = open("summary.txt", "w")
header = ("Sequence\tTotal_reads\tSingleton\tContigs_reads\tContigs\tMinAb\tMaxAb\tMinLen\tMaxLen\n")
sum.write(header)
sum.flush()

for el in seq_list:

    print "\n"+el+"\n"

    out = open(el+".txt","w")
    li = seq_list[el]
    out.write("\n".join(li))
    out.close()

    call("seqtk subseq %s %s > %s" % ("../"+fastafile, el+".txt", el+".fasta"), shell=True)

    call("cd-hit-est -T 12 -i %s -r 1 -M 0 -c 0.8 -o %s" % (el+".fasta", el+".nr80"), shell=True)

    tr = 0
    total_reads = open(el+".fasta").readlines()
    for line in total_reads:
        if line.startswith(">"):
            tr += 1

    if tr < 100000:
        call("runAssembly %s" % (el+".fasta"), shell=True)
    else:
        continue
#        call("runAssembly -large -cpu 12 %s" % (el+".fasta"), shell=True)

    elements = os.listdir(".")
    newbler_dir = [a for a in elements if a.endswith("runAssembly")]
    newbler_dir = newbler_dir[-1]

    os.chdir(newbler_dir)
    out = open("../"+el+".contigs", "w")

    #contigs
    i = 0
    lens = []
    nr = []
    allcontigs = SeqIO.parse(open("454AllContigs.fna"), "fasta")
    for s in allcontigs:
        i+=1
        desc = s.description.split()
        nreads = desc[2]
        nreads = nreads.split("=")
        nreads = nreads[1]
        out.write(">%s__%s\n%s\n" % (str(s.id), nreads, str(s.seq)))
        lens.append(len(str(s.seq)))
        nr.append(int(nreads))
    out.close()

    #singletons
    singletons = []
    read_status = open("454ReadStatus.txt").readlines()
    for line in read_status[1:]:
        info = line.split()
        read = info[0]
        status = info[1]
        if status == "Outlier" or status == "Singleton":
            singletons.append(read)
    os.chdir("../")
    call("rm -r %s" % newbler_dir, shell=True)

    out = open(el+".singletons", "w")
    out.write("\n".join(singletons))
    out.close()

    call("seqtk subseq %s.fasta %s.singletons >> %s.contigs" % (el, el, el), shell=True)

    stats = []
    stats.append(el)
    stats.append(str(tr))
    stats.append(str(len(singletons)))
    stats.append(str(i))

    try:
        stats.append(str(min(nr)))
    except:
        stats.append("0")

    try:
        stats.append(str(max(nr)))
    except:
        stats.append("0")

    try:
        stats.append(str(min(lens)))
    except:
        stats.append("0")

    try:
        stats.append(str(max(lens)))
    except:
        stats.append("0")

    sum.write("\t".join(stats))
    sum.write("\n")
    sum.flush()

sum.close()

