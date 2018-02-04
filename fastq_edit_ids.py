#!/usr/bin/python

import sys
from subprocess import call
from commands import getstatusoutput

print "Usage: fastq_edit_ids.py ListOfFastqFiles [GZ]"
print "\nFormat of the list: cosa_1.fastq(.gz) cosa_2.fastq.gz"
print "GZ: Optionally con write GZ if you prefer a .gz file as output instead of a .fastq file\n"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce FASTQ(.GZ) list name: ")

try:
    compress = sys.argv[2]
except:
    compress = "NONE"

ext = file.split(".")
extension = ext[-1]

data = open(file).readlines()

#li = open("list_checked.txt","w")

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

    identifier = id.split(":")
    identifier = identifier[0]

    if sp != -1:
        print line+" with uncorrect format, editing ids."

        awk_cmd1 = """awk '{ if (NR%4==1) { print $1"/"""
        awk_cmd2 = """" } else { print } }' """

        if extension == "fq" or extension == "fastq":
            if compress != "GZ":
                call(awk_cmd1+side+awk_cmd2+ "%s > %s" % (line, name), shell=True)
            elif compress == "GZ":
                call(awk_cmd1+side+awk_cmd2+line+" | gzip > "+name+".gz", shell=True)
        elif extension == "gz":
            if compress != "GZ":
                call("zcat " +line+ " | " +awk_cmd1+side+awk_cmd2 +"> "+ name, shell=True )
            elif compress == "GZ":
                call("zcat " +line+ " | " +awk_cmd1+side+awk_cmd2 +"| gzip > "+name+".gz", shell=True )
#        li.write(name+"\n")
        
    elif id[-2:] == "/%s" % side:
        call("ln -sf %s %s" % (line, name), shell=True)
        print line+" with the correct format, nothing happens."
#        li.write(name+"\n")
    else:
        print line+": Something wrong happens, check file."

#li.close()
