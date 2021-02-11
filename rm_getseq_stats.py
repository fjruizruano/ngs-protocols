#!/usr/bin/python

import sys
from Bio import SeqIO
from Bio.Seq import Seq

print "Usage: rm_getseq.py FastaFile RepeatMaskerOut [LenMinimum]"

try:
    fafile = sys.argv[1]
except:
    fafile = raw_input("Introduce FASTA file: ")

try:
    rmfile = sys.argv[2]
except:
    rmfile = raw_input("Introduce RepeatMasker out file: ")

try:
    lenlimit = int(sys.argv[3])
except:
    lenlimit = 0

dict_seq = {}
seqs = SeqIO.parse(fafile,"fasta")
for s in seqs:
    dict_seq[str(s.id)] = str(s.seq)

rmout = open(rmfile).readlines()
out = open(rmfile+".fas", "w")
sta = open(rmfile+".stats", "w")
sta_dict = {}

for line in rmout[3:]:
    line = line.replace("(","")
    line = line.replace(")","")
    info = line.split()
    name = info[4]
    begin_q = int(info[5])
    end_q = int(info[6])
    sense = info[8]
    id = info[9]
    begin_r = int(info[11])
    end_r = int(info[12])
    left_r = int(info[13])
    try:
        double = info[15]
    except:
        double = ""
    secu = ""
    if sense == "+" and double == "":
        len_rep = end_r-begin_r+1
        if len_rep >= lenlimit:
            secu = dict_seq[name][begin_q-1:end_q]
            out.write(">%s\n%s\n" % (name,secu))
    elif sense == "C" and double == "":
        len_rep = end_r-left_r+1
        if len_rep >= lenlimit:
            secu = dict_seq[name][begin_q-1:end_q]
            secu = Seq(secu)
            secu_inv = secu.reverse_complement()
            out.write(">%s\n%s\n" % (name,secu_inv))
    if id not in sta_dict and len(secu)>0:
        sta_dict[id] = [len(secu)]
    elif len(secu)>0:
        sta_dict[id].append(len(secu))

out.close()

sta_dict_sort = sorted(sta_dict)
for el in sta_dict_sort:
    data = sta_dict[el]
    num_el = len(data)
    av_el = sum(data)/float(num_el)
    sta.write("%s\t%s\t%s\n" % (el,str(num_el),str(av_el)))
sta.close()
