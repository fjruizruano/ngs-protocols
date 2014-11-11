#!/usr/bin/python

import sys 

try:
    data = sys.argv[1]
    names = sys.argv[2]
except:
    data = raw_input("RepeatMasker's *.out file: ")
    names = raw_input("List with names: ")

d = open(data).readlines()
n = open(names).readlines()

li = []

for i in range(0,len(n)):
    n[i] = n[1][:-1]

for line in d[3:]:
    line = line.split()
    if line[10] in n:
        li.append(line[4][:-1])

li = set(li)

w = open(names+".lst","w")
for l in li:
    w.write("%s\n%s\n" % (l+"1",l+"2"))
w.close()
