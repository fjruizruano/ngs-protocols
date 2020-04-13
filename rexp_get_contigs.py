#!/usr/bin/python
import re
import operator
from Bio import SeqIO
import os
from subprocess import call

subfol = os.walk('.').next()[1]

com = "cat "

for num in range(1,len(subfol)+1):
	n = str(num)
	while len(n) < 4:
		n = "0" + n
	com = com + "./dir_CL%s/contigs_CL%s " % (n, num)

com = com + "> out.txt"

print com

call(com, shell=True)

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
    ii = 1.0*i/2
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
