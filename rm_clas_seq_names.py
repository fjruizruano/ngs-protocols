#!/usr/bin/python

from Bio import SeqIO
from operator import itemgetter

files = open("lista_out.txt").readlines()
names = open("lista_names.txt").readlines()
names = [x[:-1] for x in names]

out_in1 = open("list_in_1.fas", "w")
out_in2 = open("list_in_2.fas", "w")
out_no1 = open("list_no_1.fas", "w")
out_no2 = open("list_no_2.fas", "w")

dict_name_1 = {}
dict_name_2 = {}
dict_annot = {}
#dict_annot_empty = {}

for name in names:
	dict_name_1[name] = open(name+"_1.fas", "w")
	dict_name_2[name] = open(name+"_2.fas", "w")
	dict_annot[name] = []
#	dict_annot_empty[name] = []

for file in files:
	print "\nLoading files %s and %s" % (file[:-1], file[:-5])
	input = open(file[:-1]).readlines()
	lista_id = []
#	dict_annot = dict_annot_empty
	for name in dict_annot:
		dict_annot[name] = []
	print dict_annot
	for line in input[3:]:
		text = line.split()
		id = text[4]
		annot = text[10]
		for name in names:
			if name in annot:
				dict_annot[name].append(id[:-1])
		lista_id.append(id[:-1])
			
	lista_id = list(set(lista_id))
	lista_id.sort()
	for name in dict_annot:
		li = dict_annot[name]
		li = list(set(li))
		li.sort()
		dict_annot[name] = li
	print "Loading sequences"	
	handle = open(file[:-5], "rU")
	sequen = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
	handle.close()
	print "Getting sequences..."
	for name in dict_annot:
		for el in dict_annot[name]:
			fas_1 = ">%s\n%s\n" % (el+"/1", str(sequen[el+"1"].seq))
			fas_2 = ">%s\n%s\n" % (el+"/2", str(sequen[el+"2"].seq))
			dict_name_1[name].write(fas_1)
			dict_name_2[name].write(fas_2)

	for el in lista_id:
		fas_1 = ">%s\n%s\n" % (el+"/1", str(sequen[el+"1"].seq))
		fas_2 = ">%s\n%s\n" % (el+"/2", str(sequen[el+"2"].seq))
		out_in1.write(fas_1)
		out_in2.write(fas_2)
		del sequen[el+"1"]
		del sequen[el+"2"]

	for el in sorted(sequen.iterkeys()):
		sec = sequen[el]
		if el[-1:] == "1":
			out_no1.write(">%s\n%s\n" % (el[:-1]+"/"+el[-1:], str(sec.seq)))
		elif el[-1:] == "2":
			out_no2.write(">%s\n%s\n" % (el[:-1]+"/"+el[-1:], str(sec.seq)))

out_in1.close()
out_in2.close()
out_no1.close()
out_no2.close()

for name in names:
	dict_name_1[name].close()
	dict_name_2[name].close()
