#!/usr/bin/python

import sys
from subprocess import call

print "divsum_count.py ListOfDivsumFiles\n"

try:
    files = sys.argv[1]
except:
    files = raw_input("Introduce RepeatMasker's list of Divsum files with library size (tab separated): ")

files = open(files).readlines()
to_join = []

header = "Coverage for each repeat class and divergence (Kimura)\n"

results = {}

for line in files:
    line = line.split("\t")
    file = line[0]
    size = int(line[1])
    data = open(file).readlines()
    matrix_start = data.index(header)
    matrix = data[matrix_start+1:]
    li= []
    names_line = matrix[0]
    info = names_line.split()

    for fam in info:
        li.append([fam])

    info_len = len(li)

    for line in matrix[1:]:
        info = line.split()
        for i in range(0,info_len):
            li[i].append(info[i])

    out = open(file+".counts","w")
    out.write("Sequence\tAbundance\n")

    stats = open(file+".stats","w")
    stats.write("Sequence\tDivergence\tTotalAbundance\tMaxAbundance\tMaxPeak\tRPS\tDIVPEAK\n")

    for el in li[1:]:
        numbers = el[1:]
        numbers = [int(x) for x in numbers]
        numbers_prop = [1.0*x/size for x in numbers]
        prop_dict = {}
        prop_li = []
        for prop in range(0,len(numbers_prop)):
            prop_dict[prop] = numbers_prop[prop]
            prop_li.append(numbers_prop[prop])
        prop_dict_sorted = sorted(prop_dict.items(), key=lambda x: x[1], reverse=True)
        total = sum(numbers_prop)
        top = prop_dict_sorted[0]
        top_div = top[0]
        top_ab = top[1]

        peak = []
        if top_div >= 2:
            for div in range(top_div-2,top_div+3):
                peak.append(prop_dict[div])
        else:
            for div in range(0,5):
                peak.append(prop_dict[div])
            
        sum_peak = sum(peak)
        rps = sum_peak/total
        divpeak = top_div
        out.write(el[0]+"\t"+str(sum(numbers))+"\n")

        all_divs = []
        for d in li[0][1:]:
            all_divs.append(int(d)+0.5)
        div_sumproduct = 0
        for x,y in zip(all_divs,prop_li):
            div_sumproduct += x * y
        divergence = div_sumproduct/total

        data = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (el[0],str(divergence),str(total),str(top_ab),str(sum_peak),str(rps),str(divpeak))
        stats.write(data)

        data2 = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (file, str(divergence),str(total),str(top_ab),str(sum_peak),str(rps),str(divpeak))

        if el[0] in results:
             results[el[0]].append(data2)
        else:
             results[el[0]] = [data2]
            
    out.close()
    stats.close()

    to_join.append(file+".counts")

out = open("results.txt", "w")

for el in sorted(results):
    info = results[el]
    out.write("%s\tDivergence\tTotalAbundance\tMaxAbundance\tMaxPeak\tRPS\tDIVPEAK\n" % (el))
    for i in info:
        out.write(i)
    out.write("\n\n\n")
out.close()

call("join_multiple_lists.py %s" % (" ".join(to_join)), shell=True)
