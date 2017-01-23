#!/usr/bin/python

import sys
import commands
from subprocess import call, Popen
from os import listdir
from os.path import isfile, join

print "sat_subfam2fam_multi.py AlignFile PatternFile Threads"

try:
    dat = sys.argv[1]
except:
    dat = raw_input("Introduce align file: ")

try:
    pat = sys.argv[2]
except:
    pat = raw_input("Introduce pattern file: ")

try:
    th = sys.argv[3]
except:
    th = raw_input("Introduce number of threads: ")

th = int(th)

c = commands.getstatusoutput("wc -l %s" % dat)
c = c[1]
c = c.split()
c = int(c[0])

lines = (c/th)+1

call("split -l %s %s %s " % (str(lines), dat, dat), shell=True)

onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
splits = []
for f in onlyfiles:
    if f.startswith(dat+"a"):
        splits.append(f)
splits.sort()

commands = []
for n in range(0,len(splits)):
    com = "sat_subfam2fam_multi_support.py %s %s" % (splits[n],pat)
    commands.append(com)

processes = [Popen(cmd, shell=True) for cmd in commands]
for p in processes:
    p.wait()

splits_fam = []

for s in splits:
    splits_fam.append(s+".fam")

call("cat %s > %s.fam" % (" ".join(splits_fam), dat), shell=True)

print splits

call("calcDivergenceFromAlign.pl -s %s.fam.divsum %s.fam" % (dat,dat), shell=True)
