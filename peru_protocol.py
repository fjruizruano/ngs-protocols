#!/usr/bin/python

import sys
from subprocess import call

print "Usage: peru_protocol.py list_out.txt FastaFile ReadLength "

try:
    list_out = sys.argv[1]
except:
    list_out = raw_input("Introduce list of OUT files from RepeatMasker: ")

try:
    fasta = sys.argv[2]
except:
    fasta = raw_input("""Introduce Fasta File with IDs in RepeatMasker format (Names in format "LmiSat01A-185#Satellite/LmiSat01A-185"): """)

try:
    read_len = sys.argv[3]
    read_len = int(read_len)
except:
    read_len = raw_input("Introduce read length: ")
    read_len = int(read_len)

limit_len = read_len - 11
limit_len = str(limit_len)

# Get pattern file 

call(""" grep ">" %s | sed 's/>//g' | sed 's/#/\t/g' | awk {'print $1'} > names.txt""" % (fasta), shell=True)

names = open("names.txt").readlines()
names_dict = {}
names_list = []

for line in names:
    name = line[:-1]
    name = name.split("-")
    if name[0].endswith("A"):
        names_dict[name[0][:-1]] = [name]
        names_list.append(name[0][:-1])
    else:
        names_dict[name[0][:-1]].append(name)

pattern = open("pattern.txt", "w")

for el in names_list:
    data = names_dict[el]
    if len(data) > 1:
        main = data[0]
        for dat in data[1:]:
            pattern.write("%s\t%s\n" % ("-".join(dat),"-".join(main)))

pattern.close()

outs = open(list_out).readlines()

for out in outs:
    out = out[:-1]

    call("replace_patterns.py %s pattern.txt" % out, shell=True)

    call("""grep -v "*" %s.fam > %s.fam.noasterisk""" % (out, out), shell=True)

    call("rm_getseq_annot.py %s %s.fam.noasterisk 1" % (out[:-4],out), shell=True)

    call("rm_count_matches_monomers.py %s.fam.noasterisk.fas %s" % (out, limit_len), shell=True)

    call("rm_cluster_external.py %s.fam.noasterisk %s pattern.txt" % (out, out[:-4]), shell=True)
