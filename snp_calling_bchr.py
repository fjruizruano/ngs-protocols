#!/usr/bin/python

import sys
import operator

print "Usage: snp_calling_bchr.py VariationFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce variation file: ")

table = open(file).readlines()

w = open("snps_selected.txt", "w")
w.write("".join(table[0:2]))

var = ["D","I","A","C","T","G"]

for line in table[2:]:
    info = line.split()
    count = [int(x) for x in info[2:8]]
    variants = {}
    for i in range(0,6):
        variants[var[i]] = count[i]
    sorted_variants = sorted(variants.items(), key=operator.itemgetter(1))
    sorted_variants.reverse()
    one = sorted_variants[0] 
    two = sorted_variants[1]
    total = [i[1] for i in sorted_variants]
    total = sum(total)
    if total != 0 and 1.0*(two[1]-1)/total > 0.1:
        w.write("\t".join(info)+"\n")
        
w.close()
