#! /usr/bin/python

import sys

try:
        inp = sys.argv[1]
        files = open(inp)
except:
        files = open("lista_out.txt")

# process RM *.out file
dict_count = {}
dict_diver = {}

header = """   SW   perc perc perc  query                                        position in query    matching             repeat        position in repeat
score   div. del. ins.  sequence                                     begin end   (left)   repeat               class/family begin  end    (left)  ID

"""

try:
        out_name = sys.argv[2]
        outout = open(out_name,"w")
except:
        outout = open("test.all.out", "w")
outout.write(header)

def process_out(file):
        file = open(file).readlines()

        for line in file[3:]:
                outout.write(line)
                text = line.split()
                begin = int(text[5])-1
                end = int(text[6])
                if end - begin > 50:
                        diver = float(text[1])
                        annot = text[9]
                        look = annot in dict_count
                        if look == True:
                                dict_count[annot] += 1
                                dict_diver[annot].append(diver)
                        elif look == False:
                                dict_count[annot] = 1
                                dict_diver[annot] = [diver]

for file in files:
        process_out(file[:-1]) #complete dictionary of counts

outout.close()

