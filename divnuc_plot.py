#!/usr/bin/python

import sys

print "Usage: divnuc_plot.py DivNucFile WindowSize"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce DivNuc file: ")

try:
    win = sys.argv[2]
except:
    win = raw_input("Introduce Window Size (integer): ")

try:
    win = int(win)
except:
    print "Please, introduce an integer as Window Size"

def average(l):
    av = reduce(lambda x,y:x+y,l)/len(l)
    return av

data = open(file).readlines()

w = open(file+".plot."+str(win), "w")

for n in range(0,len(data)/win):
    subset = data[n*win:(n*win)+win]
    cov = []
    div = []
    for pos in subset:
        pos = pos.split()
        cov.append(int(pos[2]))
        div.append(float(pos[10]))
    w.write("%s\t%s\t%s\n" % (str(n*win),str(average(cov)),str(average(div))))

w.close()
