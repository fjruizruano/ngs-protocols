#!/usr/bin/python

from Bio import AlignIO
import sys

print "Usage: align_copy_paste.py AlignFileFasta Point"

try:
    file = sys.argv[1]
except:
    raw_input = ("Introduce Alignment in FASTA format: ")

try:
    point = sys.argv[2]
except:
    raw_input = ("Introduce last nucleotide of the alignmente left side: ")

label = file[0:3] 

#open output file
out = open(file+".cut.fas","w")

#load alignment
align = AlignIO.read(open(file),"fasta")

point = int(point)

left = align[0:,:point]
right = align[0:,point:]

new_ali = right+left

i = 1

for el in new_ali:
    i_str = str(i)
    while len(i_str) < 4:
        i_str = "0" + i_str
    out.write(">%s%s\n%s\n" % (label,i_str,str(el.seq)))
    i += 1

out.close()
