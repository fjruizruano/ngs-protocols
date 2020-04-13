#!/usr/bin/python

import sys

print "divsum_join_annot.py RepeatLandscapeFile AnnotationFile" 

try:
    rl_file = sys.argv[1]
except:
    rl_file = raw_input("Introduce repeat landscape file: ")

try:
    annot_file = sys.argv[2]
except:
    annot_file = raw_input("Introduce anntation file")

rl = open(rl_file).readlines()

annot = open(annot_file).readlines()

annot_single = []
annot_dict = {}
rl_final = {}

fill = 71*"0"
zeros = []
for el in fill:
    zeros.append(int(el))

for line in annot:
    info = line.split()
    annot_dict[info[0]] = info[1]
    if info[1] not in annot_single:
        annot_single.append(info[1])
        rl_final[info[1]] = zeros

rl_db = []

header = rl[0]
header = header.split()
for el in header[1:]:
    rl_db.append([el,[]])

for el in rl[1:]:
    info = el.split()
    info = info[1:]
    for n in range(0,len(info)):
        rl_db[n][1].append(int(info[n]))

for el in rl_db:
    id = el[0]
    name = annot_dict[id]
    before = rl_final[name]
    column = el[1]
    suma = [before[i]+column[i] for i in range(len(before))]
    rl_final[name] = suma

out = open("output.txt", "w")
for el in rl_final:
    string = [str(i) for i in rl_final[el]]
    out.write("%s\t%s\n" % (el, "\t".join(string)))

out.close()

