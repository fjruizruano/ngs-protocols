#!/usr/bin/python

import sys
from subprocess import call

print "replace_patterns.py FileToModify PatternFile"

try:
    dat = sys.argv[1]
except:
    dat = raw_input("Introduce file to modify: ")

try:
    pat = sys.argv[2]
except:
    pat = raw_input("Introduce pattern file: ")

pat = open(pat).readlines()

patterns = {}

for line in pat:
    info = line.split()
    patterns[info[0]] = info[1]

data = open(dat).readlines()

w = open(dat+".fam", "w")

for line in data:
    for el in patterns:
        line = line.replace(el,patterns[el])
    w.write(line)

w.close()
