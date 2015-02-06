#!/usr/bin/python

import sys
from subprocess import call
from commands import getstatusoutput

print "Usage: fastq_edit_ids.py ListOfFastqFiles"
print "Format of the files: cosa_1.fastq(.gz) cosa_2.fastq.gz\n"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTQ(.GZ) list name: ")

ext = file.split(".")
extension = ext[-1]

data = open(file).readlines()

for line in data:
    line = line[:-1]
    print line
    ext = line.split(".")
    extension = ext[-1]

    if extension == "fq" or extension == "fastq":
        firstline = getstatusoutput("head -n 1 %s" % line)
        side = ext[-2][-1]
        name = "".join(ext[0:-1])
        name = name[:-2] + "_checked" + name[-2:] + "." +  extension
    elif extension == "gz":
        firstline = getstatusoutput("gzip -cd %s | head -n 1" % line)
        side = ext[-3][-1]
        name = "".join(ext[0:-2])
        name = name[:-2] + "_checked" + name[-2:] + "."  + ext[-2]
    id = firstline[1]
    id = id.split("\n")
    id = id[0]
    sp = id.find(" ")

    if sp != -1:
        print line+" with uncorrect format, editing ids."
        if extension == "fq" or extension == "fastq":
            call("""sed 's/%s/%s/g' %s > %s""" % (id[sp:], "\/"+side, line, name), shell=True)
        elif extension == "gz":
            call("aunpack %s" % (line), shell=True)
            call("""sed -i 's/%s/%s/g' %s && mv %s %s""" % (id[sp:], "\/"+side, line[:-3], line[:-3], name), shell=True)
    elif id[-2:] == "/%s" % side:
        call("ln -sf %s %s" % (line, name), shell=True)
        print line+" with the correct format, nothing happens."
    else:
        print line+": Something wrong happens, check file."
