#!/usr/bin/python

import sys
import operator

print "divsum_to_rl.py SamplesFile"

try:
    sam_file = sys.argv[1]
except:
    sam_file = raw_input("Introduce Samples File: ")

#loading samples file
##loading reference sample and repeat landscapes
samples = open(sam_file).readlines()
samples_rl = samples[0][:-1]
samples_rl = samples_rl.split("\t")
sp_name = samples_rl[0]
ref_library = samples_rl[1]
rep_land = samples_rl[2]

##loading divsum files
lib_dict = {}
for lib in samples[1:]:
    lib = lib[:-1]
    lib = lib.split("\t")
    lib_dict[lib[0]] = lib[1:]

#sort by abundance in  ref library

##loading divsum file
ref_divsum = lib_dict[ref_library][0]
nucs = lib_dict[ref_library][1]
nucs = int(nucs)
data = open(ref_divsum).readlines()

s_matrix = data.index("Coverage for each repeat class and divergence (Kimura)\n")
matrix = []

elements = data[s_matrix+1]
elements = elements.split()
for element in elements[1:]:
    matrix.append([element,[]])
n_el = len(matrix)

for line in data[s_matrix+2:]:
# print line
    info = line.split()
    info = info[1:]
    for n in range(0,n_el):
        matrix[n][1].append(int(info[n]))

family_abs = {}

for n in range(0,n_el):
    family_abs[matrix[n][0]] = sum(matrix[n][1])

sort_abs = sorted(family_abs.iteritems(), key=operator.itemgetter(1), reverse=True)

defnames = []

for n in range(0,len(sort_abs)):
    info = sort_abs[n]
    defnames.append([info[0], sp_name+str(n+1)])

family_abs_def = []
family_rel_def = []
for n in range(0,len(defnames)):
    number = family_abs[defnames[n][0]]
    rel_number =  round(1.0*number/nucs,100)
    family_abs_def.append([defnames[n][1],number])
    family_rel_def.append([defnames[n][1],rel_number])
    
#print family_abs_def
#print family_rel_def


#convert matrix to dictionary

matrix_abs_dict = {}

for el in matrix:
    matrix_abs_dict[el[0]] = el[1]

matrix_rel_list = []

for n in range(0,len(defnames)):
    lista = matrix_abs_dict[defnames[n][0]]
    lista_rel = [round(1.0*x/nucs,100) for x in lista]
    matrix_rel_list.append([defnames[n][1],lista_rel])

# write rel matrix
out = open("output.txt","w")

n_div = len(matrix_rel_list[0][1])
header = ["Div"]
for el in matrix_rel_list:
    header.append(el[0])

out.write("\t".join(header)+"\n")

row_names = range(0,n_div)

for a in range(0,len(row_names)):
    line = [row_names[a]]
    for b in range(0,len(matrix_rel_list)):
        line.append(matrix_rel_list[b][1][a])
    line = [str(l) for l in line]
    out.write("\t".join(line)+"\n")

out.close()

rscript = open("rscript.R","w")

script = """library(ggplot2)
library(plyr)
library(reshape2)
library(RColorBrewer)
lmig <- read.table("%s",header=T)
lm <- melt(lmig, id.vars=0:1)
colourCount = %s
ref <- colorRampPalette(brewer.pal(12, "Paired"))(colourCount)
palette1 <- rev(ref) 
ggplot(data=lm, aes(x=lm$Div, y=lm$value, fill=lm$variable))+geom_bar(stat="identity", position = position_stack(reverse = TRUE)) + scale_fill_manual(name="satDNA Families", values = palette1)+labs(x="Kimura Substitution Level (%s)", y="Genome Proportion")+theme_bw()
""" % ("output.txt", str(len(matrix_rel_list)), "%")


rscript.write(script)

rscript.close()


