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

genes_dict = {}

for line in vardata[2:]:
 data = line.split()
 gene = data[0]

 if gene in genes_dict:
  genes_dict[gene].append(line)
 else:
  genes_dict[gene] = [line]

for m in range(0,len(samples)):
 begin = 2+(m*6)
 end = 2+(m*6)+6
 for gene in genes_dict:
   seq = []
   g_lines = genes_dict[gene]
   for g_line in g_lines:
    data = g_line.split()
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
    seq.append(base)

   out.write(">%s_%s\n" % (gene,samples[m]))
#  for el in seq_dict:
#    out.write(">%s_%s\n" % (samples[m],el))
   out.write("".join(seq))
   out.write("\n")

out.close()
