#!/usr/bin/python

import sys
from subprocess import call

print "Usage: count_bases_fastq.py file_1.fq [file_2.fq file_1.fastq.gz file_2.fastq.gz]"

narg = len(sys.argv)
files = sys.argv[1:narg]

for file in files:
    extensions = file.split(".")
    if extensions[-1] == "gz":
        call("""zcat %s | paste - - - - | cut -f2 | tr -d '\n' | wc -c""" % (file), shell=True)
    elif extensions[-1] == "fq" or extensions[-1] == "fastq":
        call("""cat %s | paste - - - - | cut -f2 | tr -d '\n' | wc -c""" % (file), shell=True)
    else:
        print "Nothing happens. Please, check format and extension."
