#!/usr/bin/python

import re
import operator
from Bio import SeqIO

data = SeqIO.parse("out.txt", "fasta")

id_dict = {}

for s in data:
    info = re.split("CL|Contig|\055| ", s.description)
    CL = info[1]
    contig = info[2]
    cov = float(info[4])

    if CL in id_dict:
        id_dict[CL][contig] = cov
    else:
        id_dict[CL] = {contig : cov}

sel = {}

for el in id_dict:
    info = id_dict[el]
    info_s = sorted(info.items(), key=operator.itemgetter(1))
    info_s.reverse()
    sel[int(el)] = []
    i = 0
    for x in info_s:
        i += x[1]
    ii = 1.0*i/3
    j = 0
    for x in info_s:
        if j < ii:
           sel[int(el)].append(x[0])
        j += x[1]

sel_s = sorted(sel.items(), key=operator.itemgetter(0))

w = open("out.list","w")
for l in sel_s:
    for con in l[1]:
        w.write("CL%sContig%s\n" % (str(l[0]),con))
w.close()
