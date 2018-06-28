#!/usr/bin/python

import sys
import operator
from subprocess import call
from Bio import SeqIO

print "divsum_count.py DivsumFile FastaFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce RepeatMasker's Divsum file: ")

try:
    fasta = sys.argv[2]
except:
    fasta = raw_input("Introduce FASTA file: ")

data = open(file).readlines()

header = "Coverage for each repeat class and divergence (Kimura)\n"

matrix_start = data.index(header)
matrix = data[matrix_start+1:]
li = []
li_clean = []
names_line = matrix[0]
info = names_line.split()
info = info[1:]

for fam in info:
    fam_clean = fam.split("/")
    li.append([fam])
    li_clean.append([fam_clean[1]])

info_len = len(li)

for line in matrix[1:]:
    info = line.split()
    info = info[1:]
    for i in range(0,info_len):
        li_clean[i].append(info[i])

out = open(file+".counts","w")

counts = []
for el in li_clean:
    numbers = el[1:]
    numbers = [int(x) for x in numbers]
    counts.append([el[0],sum(numbers)])
    out.write(el[0]+"\t"+str(sum(numbers))+"\n")

out.close()

fam_count = {}
fam_all = {}
fam_members = {}
seq_list = []
var_number = {}

for el in counts:
    clase = el[0]
    count = el[1]
    clase_fam = clase.split("_")
    clase_fam = clase_fam[-1]
    if len(clase_fam) == 2:
        if clase_fam in fam_count:
            fam_members[clase_fam].append(clase)
            last_count = fam_count[clase_fam][1]
            if count > last_count:
                fam_count[clase_fam] = [clase,count]
            fam_all[clase_fam][clase] = count
        else:
            fam_members[clase_fam] = [clase]
            fam_count[clase_fam] = [clase,count]
            fam_all[clase_fam] = {clase:count}
    else:
        seq_list.append(clase)
        var_number[clase] = 1

out = open("pattern.txt", "w")

for el in fam_count:
    leader = fam_count[el][0]
    seq_list.append(leader)
    members = fam_members[el]
    var_number[leader] = len(members)
    for member in members:
        if member != leader:
            out.write("%s\t%s\n" % (member, leader))

out.close()

out = open("selection.txt", "w")
out.write("\n".join(seq_list))
out.close()

call("extract_seq.py %s selection.txt" % fasta, shell=True)

out = open("table.txt", "w")

fasta_sel = SeqIO.parse(open("selection.txt.extract"), "fasta")

for secu in fasta_sel:
    secuen = str(secu.seq)
    id = str(secu.id)
    length = len(secuen)
    at = secuen.count("A")+secuen.count("T")+secuen.count("a")+secuen.count("t")
    at_perc = float(1.0*at/length)
    v_number = var_number[id]
    out.write("%s\t%s\t%s\t%s\n" % (id, str(length), str(at_perc), v_number))

out.close()

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
abc_dict = {}
for el in fam_all:
    family = fam_all[el]
    family_sort = sorted(family.iteritems(), key=operator.itemgetter(1), reverse=True)
    i = -1
    for var in family_sort:
        i += 1
        abc_dict[var[0]] = fam_count[el][0] + abc[i]

out = open(fasta+".abc", "w")
fas = SeqIO.parse(open(fasta), "fasta")
len_dict = {}
for s in fas:
    new = s.id
    length = len(str(s.seq))
    if s.id in abc_dict:
        new = abc_dict[s.id]
    out.write(">%s-%s\n%s\n" % (new, length, s.seq))
    len_dict[new] = length
out.close()

out = open(fasta+".dim.abc", "w")
fas = SeqIO.parse(open(fasta+".dim"), "fasta")
for s in fas:
    new = s.id
    if s.id in abc_dict:
        new = abc_dict[s.id]
    length = len_dict[new]
    out.write(">%s-%s\n%s\n" % (new, length, s.seq))
out.close()

