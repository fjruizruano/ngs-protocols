#!/usr/bin/python

import sys
import operator
from subprocess import call

print "Usage: divsum_to_rl.py SamplesFile"

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

data_dict = {}

#sort by abundance in ref library

##loading divsum file
ref_divsum = lib_dict[ref_library][0]
ref_divsum = ref_divsum.replace(".divsum", ".fam.divsum")
nucs = lib_dict[ref_library][1]
nucs = int(nucs)
data = open(ref_divsum).readlines()

s_matrix_div = data.index("-----\t------\t------\t-----------\t-------\n")
s_matrix = data.index("Coverage for each repeat class and divergence (Kimura)\n")
matrix_div = []
divergence = {}
elements_div = data[s_matrix_div+1:s_matrix-2]
for line in elements_div:
    info = line.split()
    divergence[info[1]] = info[-1]

matrix = []

elements = data[s_matrix+1]
elements = elements.split()
for element in elements[1:]:
    element = element.split("/")
    element = element[-1]
    matrix.append([element,[]])
n_el = len(matrix)

big_row = 0

for line in data[s_matrix+2:s_matrix+45]:
    info = line.split()
    info = info[1:]
    for n in range(0,n_el):
        matrix[n][1].append(int(info[n]))
    suma = [int(x) for x in info]
    suma = sum(suma)
    suma_rel = 1.0*suma/nucs
    if suma_rel > big_row:
        big_row = suma_rel

family_abs = {}

for n in range(0,n_el):
    sat_name = matrix[n][0]
    family_abs[sat_name] = sum(matrix[n][1])

sort_abs = sorted(family_abs.iteritems(), key=operator.itemgetter(1), reverse=True)

#loading len information
try:
    table = open("table.txt").readlines()
    table_dict = {}
    for l in table:
        info = l.split()
        table_dict[info[0]] = info[1]
except:
    pass

defnames = []
eq_names = []

sat_digits = len(str(len(sort_abs)))
for n in range(0,len(sort_abs)):
    info = sort_abs[n]
    number_name = str(n+1)
    while len(number_name) < sat_digits:
        number_name = "0"+number_name
    monomer_len = table_dict[info[0]]
    defnames.append([info[0], sp_name+"Sat"+number_name+"-"+monomer_len])
    eq_names.append([info[0], sp_name+"Sat"+number_name])

out = open("equivalences.txt", "w")
for n in eq_names:
    out.write("%s\t%s\n" % (n[0], n[1]))
out.close()

family_abs_def = []
family_rel_def = []
for n in range(0,len(defnames)):
    number = family_abs[defnames[n][0]]
    rel_number = round(1.0*number/nucs,100)
    family_abs_def.append([defnames[n][1],number])
    family_rel_def.append([defnames[n][1],rel_number,divergence[defnames[n][0]]])

out = open(ref_library+".abdiv","w")
for el in family_rel_def:
    out.write("%s\t%s\t%s\n" % (el[0], str(el[1]), el[2]))
out.close()

#convert matrix to dictionary

matrix_abs_dict = {}

for el in matrix:
    matrix_abs_dict[el[0]] = el[1]

matrix_rel_list = []

for n in range(0,len(defnames)):
    lista = matrix_abs_dict[defnames[n][0]]
    lista_rel = [1.0*x/nucs for x in lista]
    matrix_rel_list.append([defnames[n][1],lista_rel])

data_dict[ref_library] = matrix_rel_list

# write rel matrix
out = open(ref_library+"_rl.txt","w")

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


#continue with the other libraries

##loading divsum file
if lib_dict > 1:
 for library in lib_dict:
  if library != ref_library:
   ref_divsum = lib_dict[library][0]
   ref_divsum = ref_divsum.replace(".divsum", ".fam.divsum")
   nucs = lib_dict[library][1]
   nucs = int(nucs)
   data = open(ref_divsum).readlines()

   s_matrix_div = data.index("-----\t------\t------\t-----------\t-------\n")
   s_matrix = data.index("Coverage for each repeat class and divergence (Kimura)\n")
   matrix_div = []
   divergence = {}
   elements_div = data[s_matrix_div+1:s_matrix-2]
   for line in elements_div:
    info = line.split()
    divergence[info[1]] = info[-1]

   matrix = []

   elements = data[s_matrix+1]
   elements = elements.split()
   for element in elements[1:]:
    element = element.split("/")
    element = element[-1]
    matrix.append([element,[]])
   n_el = len(matrix)

   for line in data[s_matrix+2:s_matrix+45]:
    info = line.split()
    info = info[1:]
    for n in range(0,n_el):
     matrix[n][1].append(int(info[n]))
    suma = [int(x) for x in info]
    suma = sum(suma)
    suma_rel = 1.0*suma/nucs
    if suma_rel > big_row:
     big_row = suma_rel

   family_abs = {}

   for n in range(0,n_el):
    family_abs[matrix[n][0]] = sum(matrix[n][1])

   family_abs_def = []
   family_rel_def = []
   for n in range(0,len(defnames)):
    number = family_abs[defnames[n][0]]
    rel_number =  round(1.0*number/nucs,100)
    family_abs_def.append([defnames[n][1],number])
    family_rel_def.append([defnames[n][1],rel_number,divergence[defnames[n][0]]])

   out = open(library+".abdiv","w")
   for el in family_rel_def:
    out.write("%s\t%s\t%s\n" % (el[0], str(el[1]), el[2]))
   out.close()

   #convert matrix to dictionary

   matrix_abs_dict = {}

   for el in matrix:
    matrix_abs_dict[el[0]] = el[1]

   matrix_rel_list = []

   for n in range(0,len(defnames)):
    lista = matrix_abs_dict[defnames[n][0]]
    lista_rel = [round(1.0*x/nucs,100) for x in lista]
    matrix_rel_list.append([defnames[n][1],lista_rel])

   data_dict[library] = matrix_rel_list

   # write rel matrix
   out = open(library+"_rl.txt","w")

   n_div = len(matrix_rel_list[0][1])

   out.write("\t".join(header)+"\n")

   row_names = range(0,n_div)

   for a in range(0,len(row_names)):
    line = [row_names[a]]
    for b in range(0,len(matrix_rel_list)):
     line.append(matrix_rel_list[b][1][a])
    line = [str(l) for l in line]
    out.write("\t".join(line)+"\n")

   out.close()

for library in lib_dict:

   rscript = open(library+"_rl.R","w")

   script = """library(ggplot2)
   library(plyr)
   library(reshape2)
   library(RColorBrewer)
   lmig <- read.table("%s_rl.txt",header=T)
   lm <- melt(lmig, id.vars=0:1)
   colourCount = %s
   ref <- colorRampPalette(brewer.pal(12, "Paired"))(colourCount)
   palette1 <- rev(ref)
   pdf("%s_rl.pdf")
   ggplot(data=lm, aes(x=lm$Div, y=lm$value, fill=lm$variable))+geom_bar(stat="identity", position = position_stack(reverse = TRUE)) + scale_fill_manual(name="satDNA Families", values = palette1)+labs(x="Kimura Substitution Level (%s)", y="Genome Proportion") + ylim(0,%s) +theme_bw()
   dev.off()
   """ % (library, str(len(matrix_rel_list)), library, "%", str(big_row))

   rscript.write(script)
   rscript.close()

   call("Rscript %s_rl.R" % library, shell=True)

#substractive repeat landscape
if rep_land != "NO":
 rep_land = rep_land.split(",")
 for rl in rep_land:
  data_subs = []
  pairs = rl.split("-")
  data1 = data_dict[pairs[0]]
  data2 = data_dict[pairs[1]]
  for d in range(0,len(data1)):
   sat1 = data1[d][1]
   sat2 = data2[d][1]
   data_subs.append([data1[d][0], [a-b for a,b in zip(sat1,sat2)]])
  
  # write rel matrix
  out = open(rl+"_rl.txt","w")

  n_div = len(data_subs[0][1])

  out.write("\t".join(header)+"\n")

  row_names = range(0,n_div)

  for a in range(0,len(row_names)):
   line = [row_names[a]]
   for b in range(0,len(data_subs)):
    line.append(data_subs[b][1][a])
   line = [str(l) for l in line]
   out.write("\t".join(line)+"\n")

  out.close()

  rscript = open(rl+"_rl.R","w")

  script = """library(ggplot2)
  library(plyr)
  library(reshape2)
  library(RColorBrewer)


  subs <- read.table("%s_rl.txt",header=T)
  s <- melt(subs, id.vars=0:1)
  s1 <- subset(s,s$value>=0)
  s2 <- subset(s,s$value<0)
  colourCount = %s
  ref <- colorRampPalette(brewer.pal(12, "Paired"))(colourCount)
  palette1 <- rev(ref)
  pdf("%s_rl.pdf")
  ggplot()+geom_bar(data=s2,aes(x=s2$Div, y=s2$value, fill=s2$variable),stat="identity",position=position_stack(reverse = TRUE))+scale_fill_manual(name="satDNA Families", values=palette1)+labs(x="Kimura Substitution Level (%s)", y="Genome Proportion")+theme_bw() + geom_bar(data=s1,aes(x=s1$Div, y=s1$value, fill=s1$variable),stat="identity",position=position_stack(reverse = TRUE))+scale_fill_manual(name="satDNA Families", values=palette1)+labs(x="Kimura Substitution Level (%s)",y="Genome Proportion")+theme_bw()
  dev.off()
  """ % (rl, str(len(matrix_rel_list)), rl, "%", "%")

  rscript.write(script)
  rscript.close()

  call("Rscript %s_rl.R" % rl, shell=True)

