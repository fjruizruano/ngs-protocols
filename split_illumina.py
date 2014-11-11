#!/usr/bin/python

# usage message
usage = """Usage:
repeat_masker_run.py [FASTA FILE]"""

import sys

if len(sys.argv) != 2:
	print usage
	exit(1)

file = sys.argv[1]

try:
	open(file, "r")
except IOError:
	print "Error! " + file + "does not exist, or is not readable!"
	exit(1)

file_r = open(file, "r").readlines()
len_file = len(file_r)
filename = file.split(".")
filename = filename[0]

number = 3000000

i = 0
j = 0

total_files = (len_file/number)+1

for f in range(0,total_files):
	fc = str(f)
	while len(fc) < len(str(total_files)):
		fc = ["0"] + [fc]
		fc = "".join(fc)
	f_name = "%s_%s.fas" % (filename, fc)
	out = open(f_name, "w")
	text = file_r[number*f:number*(f+1)]
	text = "".join(text)
	out.write(text)
	out.close()
