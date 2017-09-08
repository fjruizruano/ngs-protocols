#!/usr/bin/python

import sys
import operator

print "bam_consensus.py VariationFile"

try:
    varfile = sys.argv[1]
except:
    varfile = raw_input("Introduce Variation File: ")

vardata = open(varfile).readlines()

header = vardata[0]
samples = header.split()

keys = {0:"N",1:"N",2:"A",3:"C",4:"T",5:"G"}

out = open("output.txt", "w")

for m in range(0,len(samples)):
  seq_dict = {}
  begin = 2+(m*6)
  end = 2+(m*6)+6
  for line in vardata[2:]:
    data = line.split()
    nums = [int(x) for x in data[begin:end]]
    nums_dict = {}
    for n in range(0,6):
        nums_dict[n] = nums[n]
    sorted_nums = sorted(nums_dict.items(), key=operator.itemgetter(1))
    nucleotide = sorted_nums[5][0]
    abundance = sorted_nums[5][1]
    if abundance == 0:
        nucleotide = 0 # nucleotide is an "N"
    base = keys[nucleotide]
    if data[0] in seq_dict:
        seq_dict[data[0]].append(base)
    else:
        seq_dict[data[0]] = [base]
  for el in seq_dict:
    out.write(">%s_%s\n" % (samples[m],el))
    out.write("".join(seq_dict[el]))
    out.write("\n")

out.close()
