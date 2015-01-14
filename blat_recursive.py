#!/usr/bin/python

import sys
from subprocess import call, Popen
from os import listdir
from os.path import isfile, join

try:
    threads = sys.argv[1]
except:
    threads = raw_input("Introduce number of threads: ")

try:
    li = sys.argv[2]
except:
    li = raw_input("Introduce list name: ")

try:
    db = sys.argv[3]
except:
    db = raw_input("Introduce DB in FASTA format: ")

thr = int(threads)
lis = open(li).readlines()

for file in lis:
    file = file[:-1]
    call("faSplit sequence %s %s tmp_queries_" % (file, thr), shell=True)
    onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
    splits = []
    for f in onlyfiles:
        if f.startswith("tmp_queries_") and f.endswith(".fa"):
            splits.append(f)
    splits.sort()
    commands = []
    for n in range(0,len(splits)):
        com = "blat %s %s %s" % (splits[n],db,splits[n]+".blat")
        commands.append(com)

    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes:
        p.wait()
    w = open(file+".blat", "w")
    blat = open(splits[0]+".blat").readlines()
    w.write("".join(blat))
    for n in range(1,len(splits)):
        blat = open(splits[n]+".blat").readlines()
        w.write("".join(blat[5:]))
    w.close()

call("rm tmp_queries_*", shell=True)
