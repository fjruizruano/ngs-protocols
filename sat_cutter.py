#!/usr/bin/python

from Bio import AlignIO
import sys

print "Usage: sat_cutter.py AlignFileFasta"

try:
    file = sys.argv[1]
except:
    raw_input = ("Introduce Alignment in FASTA format: ")

#open output file
out = open(file+".cut.fas","w")

#load alignment
align = AlignIO.read(open(file),"fasta")

#get reference sequence
ref = str(align[0].seq)
len_ref = len(ref.replace("-",""))

#get middle point
i = -1
for col in range(0,len(ref)):
    if ref[col] != "-":
        i += 1
        if i == len_ref/2:
            point = col

#split alignment in two
left = align[0:,:point]
right = align[0:,point:]

#get reference sequence in both alignment
ref_left = str(left[0].seq)
ref_right = str(right[0].seq)

#for the remaining sequences...
for n in range(1,len(left)):
    #load sequence form left alignment
    sequen = str(left[n].seq)
    #get number or hyphens in 5-prime end
    hyphens = 0
    for nuc in sequen:
        if nuc == "-":
            hyphens += 1
        else:
            break
    #get number of nucleotides in left reference
    ref_left_nuc = len(ref_left[:hyphens].replace("-",""))
    #get cut point for right alignment
    ref_right_nuc = 0
    cut = 0
    for nuc in range(0,len(ref_right)):
        if ref_right[nuc] != "-":
            ref_right_nuc += 1
            if ref_right_nuc == ref_left_nuc:
                cut = nuc
    #write processed sequence
    final_seq = str(right[n][:cut+1].seq)+str(sequen[hyphens:])
    out.write(">%s\n%s\n" % (str(left[n].id),final_seq))

out.close()

print "WE ARE DONE!"
