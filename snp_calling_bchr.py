#!/usr/bin/python

import sys
import operator
from subprocess import call

print "Usage: snp_calling_bchr.py BamSampleFile VariationFile"

try:
    samples = sys.argv[1]
except:
    samples = raw_input("Introduce file with BAM files and sample information: ")

try:
    file = sys.argv[2]
except:
    file = raw_input("Introduce variation file: ")

sample_dict = {}
sample_list = []

samples = open(samples).readlines()

for s in samples:
    info = s.split()
    name = info[0]
    name = name.split(".")
    name = ".".join(name[:-1])
    type = info[1]
    sample_list.append(name)
    sample_dict[type] = name

table = open(file).readlines()

w = open("snps_selected.txt", "w")
w.write("\t\t"+"\t\t".join(sample_list)+"\t\n")
w.write("sequence\tpos\t"+"\t".join(["Ref","Alt"]*len(sample_list))+"\n")

n_samples = len(sample_list)

dictio = {}

for line in table[2:]:
    info = line.split()
    seq = info[0]
    pos = info[1]
    var = {}
    for i in range(0,len(sample_list)):
        index = (i*6)+2
        counts = [int(x) for x in info[index:index+6]]
        var[sample_list[i]] = counts
    dictio[seq+"."+pos] = var

ref_dict = {}

#keys = {1:"D",2:"I",3:"A",4:"C",5:"T",6:"G"}

for el in dictio:
    counts = dictio[el]["gdna_zerob"]
    total = sum(counts)
    for i in range(0,len(counts)):
        if counts[i] == total and total > 1:
            ref_dict[el] = i

alt_dict = {}

for el in ref_dict:
    ref = ref_dict[el]
    counts = dictio[el]["gdna_plusb"]
    num_ref = counts[ref]
    if num_ref == 0:
        num_ref = 1
    counts_exc = counts[:ref] + [0] + counts[ref+1:]
    maxim = max(counts_exc)
    for i in range(0,len(counts)):
        if maxim >1 and counts_exc[i] == maxim and 1.0*maxim/num_ref > 0.1:
            alt_dict[el] = i

for el in alt_dict:
    sel = dictio[el]
    ref = ref_dict[el]
    alt = alt_dict[el]
    seq_name = el.split(".")
    seq_name = "\t".join(seq_name)
    final_list = []
    for s in sample_list:
        r = sel[s][ref] 
        a = sel[s][alt]
        final_list.append(str(r))
        final_list.append(str(a))
    w.write("%s\t%s\n" % (seq_name,"\t".join(final_list)))

w.close()

call("(head -n 2 snps_selected.txt && tail -n +3 snps_selected.txt | sort -k 1,1 -k 2n) > snps_selected2.txt ", shell=True)

w = open("ref_alt.txt","w")

for el in alt_dict:
    r = ref_dict[el]
    a = alt_dict[el]
    seq_name = el.split(".")
    seq_name = "\t".join(seq_name)
    w.write("%s\t%s\t%s\n" % (seq_name,str(r),str(a)))
w.close()

call("sort -k 1,1 -k 2n ref_alt.txt > ref_alt2.txt", shell=True)
