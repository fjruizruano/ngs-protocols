#!/usr/bin/python

import sys
import operator

print "bam_consensus.py VariationFile"

try:
    varfile = sys.argv[1]
except:
    varfile = raw_input("Introduce Variation File: ")

vardata = open(varfile).readlines()

keys = {0:"N",1:"N",2:"A",3:"C",4:"T",5:"G"}

seq_dict = {}

out = open("output.txt", "w")

for line in vardata[2:]:
    data = line.split()
    nums = [int(x) for x in data[2:]]
    nums_dict = {}
    for n in range(0,6):
        nums_dict[n] = nums[n]
    sorted_nums = sorted(nums_dict.items(), key=operator.itemgetter(1))
    nucleotide = sorted_nums[5][0]
    base = keys[nucleotide]
    if data[0] in seq_dict:
        seq_dict[data[0]].append(base)
    else:
        seq_dict[data[0]] = [base]

for el in seq_dict:
    out.write(">%s\n" % (el))
    out.write("".join(seq_dict[el]))
    out.write("\n")

out.close()
