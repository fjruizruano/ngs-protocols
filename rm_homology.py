#!/usr/bin/python

import sys
from Bio import SeqIO
from subprocess import call

print "Usage: rm_homology.py FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTA file: ")

data = SeqIO.parse(open(file), "fasta")
seq_dict = {}
seq_list = []

for s in data:
    seq_dict[str(s.id)] = str(s.seq)
    seq_list.append(str(s.id))

w = open(file+"homology", "w")
w.close()

for seq in seq_list:
    tmp_list = [x for x in seq_list if x != seq]
    tmp_out = "EMPTY"

    w = open("output", "a")
    w.write(seq+":\n")
    w.close()

    while tmp_out[0] != "There were no repetitive sequences detected in tmp_query.fas\n":
        tmp_query = open("tmp_query.fas", "w")
        tmp_db = open("tmp_db.fas", "w")
        tmp_query.write(">%s\n%s\n" % (seq, seq_dict[seq]))
        tmp_query.close()

        for tmp in tmp_list:
            tmp_db.write(">%s\n%s\n" % (tmp, seq_dict[tmp])) 
        tmp_db.close()

        call("RepeatMasker -nolow -no_is -s -engine crossmatch -lib tmp_db.fas tmp_query.fas", shell=True)
        
        tmp_out = open("tmp_query.fas.out").readlines()
        print tmp_out
        call("rm -r tmp_query.fas.*", shell=True)
        if len(tmp_out) > 1:
            for line in tmp_out[3:]:
                info = line.split()
                name = "%s#%s" % (info[9],info[10])
                print name
                w = open("output", "a")
                w.write("--"+name+"\n")
                w.close()
                try:
                    tmp_list.remove(name)
                except:
                    pass
