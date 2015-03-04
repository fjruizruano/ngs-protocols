#!/usr/bin/python
import sys
from subprocess import call
from commands import getstatusoutput
import operator

file = sys.argv[1] 

data = open(file).readlines()

dictio = {}

for line in data:
    kmer = line[:-1]
    num = getstatusoutput("jellyfish query mer_counts.jf %s" % kmer)
    num = num[1]
    num = num.split()
    num = int(num[1])
    if num > 0:
        dictio[kmer] = num

sorted_dictio = sorted(dictio.items(), key=operator.itemgetter(1))

sorted_dictio.reverse()

w = open("salida.txt","w")

for el in sorted_dictio:
    w.write("%s\t%s\n" % (el[0],str(el[1])))

w.close()
