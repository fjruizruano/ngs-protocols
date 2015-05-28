#!/usr/bin/python

import sys
from subprocess import call

print "sat_subfam2fam.py AlignFile PatternFile"

try:
    dat = sys.argv[1]
except:
    dat = raw_input("Introduce align file: ")

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

call("calcDivergenceFromAlign.pl -s %s.fam.divsum %s.fam" % (dat,dat), shell=True)
