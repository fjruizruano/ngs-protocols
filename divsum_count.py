#!/usr/bin/python

import sys
from subprocess import call

print "divsum_count.py ListOfDivsumFiles"

try:
    files = sys.argv[1]
except:
    files = raw_input("Introduce RepeatMasker's Divsum file: ")

files = open(files).readlines()
to_join = []

header = "Coverage for each repeat class and divergence (Kimura)\n"

for file in files:
    file = file[:-1]
    data = open(file).readlines()
    matrix_start = data.index(header)
    matrix = data[matrix_start+1:]
    li= []
    names_line = matrix[0]
    info = names_line.split()

    for fam in info:
        li.append([fam])

    info_len = len(li)

    for line in matrix[1:]:
        info = line.split()
        for i in range(0,info_len):
            li[i].append(info[i])

    out = open(file+".counts","w")

    for el in li:
        numbers = el[1:]
        numbers = [int(x) for x in numbers]
        out.write(el[0]+"\t"+str(sum(numbers))+"\n")

    out.close()

    to_join.append(file+".counts")

call("join_multiple_lists.py %s" % (" ".join(to_join)), shell=True)
