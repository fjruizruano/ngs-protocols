#!/usr/bin/python2

import sys
from subprocess import call

try:
    li = sys.argv[1]
except:
    li = raw_input("Introduce list of input files: NAME REF FASTQ1 FASTQ2")

try:
    co = sys.argv[2]
except:
    co = raw_input("Introduce configuration file")

novo_path = "/home/fruano/private/src/NOVOPlasty4/NOVOPlasty4.3.1.pl"

li = open(li).readlines()
co = open(co).readlines()

co_dict = {"name":0, "ref":0, "fq1":0, "fq2":0}

i = -1

for line in co:
    i += 1
    if line.startswith("Project name"):
        co_dict["name"] = i
    elif line.startswith("Seed Input"):
        co_dict["ref"] = i
    elif line.startswith("Forward reads"):
        co_dict["fq1"] = i
    elif line.startswith("Reverse reads"):
        co_dict["fq2"] = i
    elif line.startswith("Output path"):
        print line
        out = line.split()
        print out
        try:
            call("mkdir " + out[-1], shell=True)
        except:
            pass
   
for line in li:
    line = line.split()
    print line
    n = line[0]
    r = line[1]
    f1 = line[2]
    f2 = line[3]

    i = -1
    w = open("config_mod.txt", "w")
    for line in co:
        i += 1
        if i == co_dict["name"]:
            line = line[:-1]+n+"\n"
        elif i == co_dict["ref"]:
            line = line[:-1]+r+"\n"
        elif i == co_dict["fq1"]:
            line = line[:-1]+f1+"\n"
        elif i == co_dict["fq2"]:
            line = line[:-1]+f2+"\n"
        w.write(line)
        print line
    w.close()
    print n
    print "%s -c config_mod.txt" % novo_path
    call("%s -c config_mod.txt" % novo_path, shell=True)
