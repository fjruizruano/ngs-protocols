#!/usr/bin/python

import sys

try:
    data = sys.argv[1]
except:
    data = raw_input("Introduce bed file: ")

# loading bed file
data = open(data).readlines()

# getting the number of libraries in the bed file
col = data[1]
col = col.split()
col = len(col) - 3

# getting header
header = data[0]
header = header.split()
header = "name\t"+ "\t".join(header[3:]) + "\n"

# opening dictionary with counts by sequence name
di = {}

# each line in the bed file
for x in data[1:]:
    # list to get the counts of this line
    counts = []
    # getting date of this line
    dat = x.split()
    name = dat[0]
    start = int(dat[1])
    end = int(dat[2])
    # filling list with counts from each library
    for count in range(1,col+1):
        counts.append(float(dat[count+2])*(end-start))
    look = name in di
    if look == True:
#        counts_old = []
        counts_old = di[name]
        di[name] = [x + y for x, y in zip(counts_old, counts)]
    else:
        di[name] = counts

w = open("count_by_seq.txt", "w")
w.write(header)
for cosa in di:
    w.write("%s\t%s\n" % (cosa, "\t".join(str(int(x)) for x in di[cosa])))
w.close()
