#!/usr/bin/python

import sys
import numpy as np

print "Usage: repeat_landscape_decimal.py AlignFile"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce Align File from RepeatMasker: ")

align = open(file).readlines()

check_name = 0
length = 0
annotation = ""

divs_zero_list = []

for i in np.arange(0,70.1,0.5):
    i = round(i,1)
    i = str(i)
    divs_zero_list.append(i)

#print divs_zero_list 

data = {}

for line in align:
    info = line.split(" ")

    try:
        check_name = int(info[0])
    except:
        check_name = 0

    if check_name > 0:
        info_5 = int(info[5])
        info_6 = int(info[6])
        length = 1+info_6-info_5

        info_8 = info[8]
        info_9 = info[9]
        if info_8 != "C":
            annotation = info_8
            annotation = annotation.split("#")
            annotation = annotation[1]
        else:
            annotation = info_9
            annotation = annotation.split("#")
            annotation = annotation[1]
        if annotation not in data:
            data[annotation] = {} 
            for i in np.arange(0,70.1,0.5):
                i = round(i,1)
                i = str(i)
                data[annotation][i] = 0

    if info[0] == "Kimura":
        div = info[-1]
        div = div[0:-2]
        div = float(div)
        div = div-(div%0.5)
        div = str(div)
        data[annotation][div] += length

out = open(file + ".decimal", "w")

header = "Div\t" + "\t".join(divs_zero_list) + "\n"
out.write(header)

for el in data:
    collect = [el]
    data_el = data[el]
    for i in divs_zero_list:
        collect.append(str(data_el[i]))
    out.write("\t".join(collect)+"\n")
    
out.close()
