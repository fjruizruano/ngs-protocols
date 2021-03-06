#!/usr/bin/python

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from subprocess import call

print "Usage: rm_getseq.py FastaFile RepeatMaskerOut BeginningShorteningLength EndShorteningLength [LenMinimum]"

try:
    fafile = sys.argv[1]
except:
    fafile = raw_input("Introduce FASTA file: ")

try:
    rmfile = sys.argv[2]
except:
    rmfile = raw_input("Introduce RepeatMasker out file: ")

try:
    begin_shortlen = int(sys.argv[3])
except:
    begin_shortlen = 0

try:
    end_shortlen = int(sys.argv[4])
except:
    end_shortlen = 0
end_shortlen = (-1*end_shortlen)-1

try:
    lenlimit = int(sys.argv[5])
except:
    lenlimit = 0

#a = "HWI-D00111:192:C39DEACXX:1:1101:2305:2139/1"
#b = a[begin_shortlen:end_shortlen]
#print begin_shortlen
#print end_shortlen
#print a
#print b

dict_seq = {}
seqs = SeqIO.parse(fafile,"fasta")
for s in seqs:
    dict_seq[str(s.id)] = str(s.seq)

rmout = open(rmfile).readlines()
out = open(rmfile+".fas", "w")

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
            out.write(">%s_%s\n%s\n" % (id,name,secu))
    elif sense == "C" and double == "":
        len_rep = end_r-left_r+1
        if len_rep >= lenlimit:
            secu = dict_seq[name][begin_q-1:end_q]
            secu = Seq(secu)
            secu_inv = secu.reverse_complement()
            out.write(">%s_%s\n%s\n" % (id,name,secu_inv))

out.close()


dict_seq = {} #clear dict_seq

call("""grep ">" %s.fas | awk -F "_" {'print $1'} | sort | uniq | sed 's/>//g' > names.txt""" % (rmfile), shell=True)

names = open("names.txt").readlines()
name_files = {}

for name in names:
    name = name[:-1]
    name_files[name] = open(name+".fas", "w")

fafile = open(rmfile+".fas")

seqs = SeqIO.parse(fafile,"fasta")
for s in seqs:
    iden = str(s.id)
    secu = str(s.seq)
    split_iden = iden.split("_")
    annot = split_iden[0]
    short_iden = split_iden[1]+"x"
    short_iden = short_iden[begin_shortlen:end_shortlen]
    name_files[annot].write(">%s_%s\n%s\n" % (annot,short_iden, secu))

for name in names:
    name = name[:-1]
    name_files[name].close()
