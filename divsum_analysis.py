#!/usr/bin/python

import sys

print "divsum_analysis.py DivsumFile NumberOfNucleotides"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce RepeatMasker's Divsum file: ")

try:
    nucs = sys.argv[2]
except:
    nucs = raw_input("Introduce number of analysed nucleotides: ")

nucs = int(nucs)

data = open(file).readlines()

s_matrix = data.index("Coverage for each repeat class and divergence (Kimura)\n")

matrix = []

elements = data[s_matrix+1]
elements = elements.split()
for element in elements[1:]:
    matrix.append([element,[]])
n_el = len(matrix)

for line in data[s_matrix+2:]:
#    print line
    info = line.split()
    info = info[1:]
    for n in range(0,n_el):
        matrix[n][1].append(int(info[n]))

abs = open(file+".abs", "w")
rel = open(file+".rel", "w")
        
for n in range(0,n_el):
    abs.write("%s\t%s\n" % (matrix[n][0], sum(matrix[n][1])))
    rel.write("%s\t%s\n" % (matrix[n][0], round(1.0*sum(matrix[n][1])/nucs,100)))

