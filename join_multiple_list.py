#!/usr/bin/python

import sys

files = sys.argv[1:]

di = {}
elements = []

for file in files:
    di[file] = {}
    data = open(file).readlines()
    for line in data:
        info = line.split()
        di[file][info[0]] = info[1]
        elements.append(info[0])

di_all = {}

for el in elements:
    di_all[el] = []
    for file in files:
        if el in di[file]:
            di_all[el].append(di[file][el])
        else:
            di_all[el].append("0")

w = open("toico.txt","w")

for el in di_all:
    w.write("%s\t%s\n" % (el, "\t".join(di_all[el])))

w.close()
