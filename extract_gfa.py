#!/usr/bin/python2

import sys
from subprocess import call

print "Usage extract_gfa.py FastaFile LookFile"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input("Introduce Fasta file: ")

try:
    look = sys.argv[2]
except:
    look = raw_input("Introduce Look file from Meryl: ")

fasta_name = fasta.split(".")
fasta_name = fasta_name[:-1]
fasta_name = ".".join(fasta_name)

look_name = look.split(".")
look_name = look_name[:-1]
look_name = ".".join(look_name)

#ext_code = """awk \134
#  'BEGIN \134
#   { \134
#     FS="[ \134t]+"; OFS="\134t"; \134
#     print "node       length        mat     pat     mat:pat color"; \134
#   } \134
#   $1 != "Assembly" \134
#   { color = "#AAAAAA"; \134
#      if ($4+$6 > 1000) { \134
#         if      ($4 > ($4+$6)*0.9) { color = "#FF8888"; } \134
#         else if ($6 > ($4+$6)*0.9) { color = "#8888FF"; } \134
#         else { color = "#FFFF00"; } \134
#      } \134
#      print $1, $2, $4, $6, $4 ":" $6, color; \134
#   }' %s > %s.color.txt""" % (look, look_name)
#call(ext_code, shell=True)

look_data = open(look).readlines()
color_out = open(look_name+".color.txt","w")
color_out.write("node\tlength\tmat\tpat\tmat:pat\tcolor\n")

for line in look_data:
    info = line.split("\t")
    name = info[0]
    length = int(info[1])
    mat = int(info[3])
    pat = int(info[5])
    color = "#AAAAAA"
    print name+" "+str(1.0*mat/length)
    if 1.0*mat/length > 0.03:
        color = "#FF8888"
    color_out.write("%s\t%s\t%s\t%s\t%s:%s\t%s\n" % (name,str(length),str(mat),str(pat),str(mat),str(pat),color))

color_out.close()

getseq = """grep "#FF8888" %s.color.txt | awk {'print $1'} > %s.color.sel.txt""" % (look_name, look_name)
call(getseq, shell=True)

extract = """seqtk subseq %s %s.color.sel.txt > %s.sel.fasta""" % (fasta, look_name, fasta_name)
call(extract, shell=True)

out = open(fasta_name+".sel.csv", "w")
out.write("node\tassignment\tlength\tinfo\tcolor\n")
out.close()
getcsv = """grep "#FF8888" %s.color.txt | awk {'print $1 "\tMATERNAL\t" $2 "\tm" $3 ":p" $4 "\t" $6'} >> %s.sel.csv""" % (look_name, fasta_name)
call(getcsv, shell=True)

