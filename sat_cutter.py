#!/usr/bin/python

from Bio import AlignIO
import sys

print "Usage: sat_cutter.py AlignFileFasta"

try:
    file = sys.argv[1]
except:
    raw_input = ("Introduce Alignment in FASTA format: ")

out = open(file+".cut.fas","w")

align = AlignIO.read(open(file),"fasta")

ref = str(align[0].seq)
len_ref = len(ref.replace("-",""))

i = -1

#get middle point
for col in range(0,len(ref)):
    if ref[col] != "-":
        i += 1
        if i == len_ref/2:
            point = col

left = align[0:,:point]
right = align[0:,point:]

ref_left = str(left[0].seq)
ref_right = str(right[0].seq)

for n in range(1,len(left)):
    sequen = str(left[n].seq)
    hyphens = 0
    for nuc in sequen:
        if nuc == "-":
            hyphens += 1
        else:
            break
    ref_left_ch = len(ref_left[:hyphens].replace("-",""))
    ref_right_ch = 0
    cut = 0
    for nuc in range(0,len(ref_right)):
        if nuc != "-":
            ref_right_ch += 1
        if ref_right_ch == ref_left_ch:
            cut = nuc
    final_seq = str(right[n][:cut].seq)+str(sequen[hyphens:])
    out.write(">%s\n%s\n" % (str(left[n].id),final_seq))

out.close()
