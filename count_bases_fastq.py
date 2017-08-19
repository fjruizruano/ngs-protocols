#!/usr/bin/python

import sys
from subprocess import call
from commands import getstatusoutput

print "Usage: count_bases_fastq.py file_1.fq [file_2.fq file_1.fastq.gz file_2.fastq.gz]"

narg = len(sys.argv)
files = sys.argv[1:narg]

output = open("count_bases.txt","w")
output.write("file\tnumber of bases\n")
print "file\tnumber of bases"

for file in files:
    n_nucs = ""
    extensions = file.split(".")
    if extensions[-1] == "gz":
        n_nucs = getstatusoutput("""zcat %s | paste - - - - | cut -f2 | tr -d '\n' | wc -c""" % (file))
    elif extensions[-1] == "fq" or extensions[-1] == "fastq":
        n_nucs = getstatusoutput("""cat %s | paste - - - - | cut -f2 | tr -d '\n' | wc -c""" % (file))
    else:
        print "Nothing happens. Please, check format and extension."
    print "%s\t%s" % (file, n_nucs[1])
    output.write("%s\t%s\n" % (file, n_nucs[1]))

output.close()
