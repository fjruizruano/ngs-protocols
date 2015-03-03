#!/usr/bin/python

import sys

file = open(sys.argv[1]).readlines()

w = open(sys.argv[1]+".fas","w")

i = 0

for line in file:
    i += 1
    line = line.split()
    w.write(">%s\n%s\n" % (str(i), line[0]))

w.close()
