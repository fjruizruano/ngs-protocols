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

li = open("list_checked.txt","w")

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

    identifier = id.split(".")
    identifier = identifier[0]

    if sp != -1:
        print line+" with uncorrect format, editing ids."
        if extension == "fq" or extension == "fastq":
            call("fastool --append /%s %s > %s" % (side, line, name), shell=True)
        elif extension == "gz":
            call("zcat %s | fastool --append /%s > %s" % (line,side,name), shell=True)
        call("""sed 's/>%s/%s/g' %s > %s.tmp""" % (identifier[1:],identifier,name,name), shell=True)
        call("mv %s.tmp %s" % (name,name), shell=True)
        li.write(name+"\n")
        
    elif id[-2:] == "/%s" % side:
        call("ln -sf %s %s" % (line, name), shell=True)
        print line+" with the correct format, nothing happens."
        li.write(name+"\n")
    else:
        print line+": Something wrong happens, check file."

li.close()
