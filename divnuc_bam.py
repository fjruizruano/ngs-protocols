#!/usr/bin/python

import sys
import operator
from subprocess import call
from Bio import SeqIO

print "Usage: divnuc_bam.py Reference BamFile"

try:
    ref = sys.argv[1]
except:
    ref = raw_input("Introduce FASTA file as reference: ")

try:
    bam = sys.argv[2]
except:
    bam = raw_input("Introduce BAM File: ")

call("pysamstats -f %s --type variation %s > %s.var" % (ref,bam,bam), shell=True)

#Selected columns in the pysamstats output
#id,pos,cov,del,ins,A,C,T,G,N
columns = [1,2,4,10,12,14,16,18,20,22]
awk_cols = []
for c in columns:
    awk_cols.append("$"+str(c))
awk_cols_str = ",\042\\t\042,".join(awk_cols)
awk_command = """awk '{print %s}' %s.var > %s.var.simple""" % (awk_cols_str,bam,bam)
call(awk_command,shell=True)

#Create dictionary with reference lengths
len_dict = {}
ref_seq = SeqIO.parse(open(ref),"fasta")
for s in ref_seq:
    nrep = s.id
    nrep = nrep.split("_")
    nrep = int(nrep[-1])
    len_dict[s.id] = [len(s.seq), nrep]

#Create dictionary with abundace per seq and position
ab_dict = {}
simple = open(bam+".var.simple").readlines()
for line in simple[1:]:
    data = line.split()
    id = data[0]
    pos = int(data[1])
    numbers = [int(x) for x in data[2:]]
    real_pos = 1+((pos-1)%(len_dict[id][0]/len_dict[id][1])) # change for reading in the id
    if id in ab_dict:
        if real_pos in ab_dict[id]:
            numbers = [x+y for x,y in zip(ab_dict[id][real_pos],numbers)]
        ab_dict[id][real_pos] = numbers
    else:
        ab_dict[id] = {real_pos:numbers}

ab_dict_sorted = sorted(ab_dict.items(), key=operator.itemgetter(0))

#print ab_dict_sorted

w = open("%s.fixed" % (bam),"w")

for l in ab_dict_sorted:
    for ll in l[1]:
        j = [l[0],ll]
        j = j+l[1][ll]
        j = [str(i) for i in j]
        w.write("\t".join(j)+"\n")

w.close()

call("./divnuc.py %s.fixed" % (bam), shell=True)
