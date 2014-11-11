#!/usr/bin/python

import sys

file1 = open(sys.argv[1]).readlines()
file2 = open(sys.argv[2]).readlines()

dict1 = {}
dict2 = {}
dicta = {}

for el in file1:
	sp = el.split("\t")
	dict1[sp[0]] = sp[1][:-1]

for el in file2:
	sp = el.split("\t")
	dict2[sp[0]] = sp[1][:-1]

elements = list(set(dict1.keys() + dict2.keys()))

for el in elements:
	dicta[el] = []
	if el in dict1:
		dicta[el].append(dict1[el])
	else:
		dicta[el].append("NA NA")

	if el in dict2:
		dicta[el].append(dict2[el])
	else:
		dicta[el].append("NA NA")

dicta2 = sorted(dicta.iterkeys())

out = open("salida.txt", "w")
out.write("Name\t%s \t%s \n" % (sys.argv[1], sys.argv[2]))

for el in dicta2:
	out.write("%s\t%s\t%s\n" % (el, dicta[el][0], dicta[el][1]))

out.close()
