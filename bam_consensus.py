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

out = open("output.txt", "w")

for line in vardata[2:]:
    data = line.split()
    nums = [int(x) for x in data[2:]]
    nums_dict = {}
    for n in range(0,6):
        nums_dict[n] = nums[n]
    sorted_nums = sorted(nums_dict.items(), key=operator.itemgetter(1))
    nucleotide = sorted_nums[5][0]
    out.write(keys[nucleotide])

print sorted_nums
print nucleotide
print keys[nucleotide]

out.close()
