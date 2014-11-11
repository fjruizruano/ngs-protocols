#!/usr/bin/python

from Bio import SeqIO

files = open("lista_out.txt").readlines()

out_in1 = open("list_in_1.fas", "w")
out_in2 = open("list_in_2.fas", "w")
out_no1 = open("list_no_1.fas", "w")
out_no2 = open("list_no_2.fas", "w")

for file in files:
	print "\nLoading files %s and %s" % (file[:-1], file[:-5])
	input = open(file[:-1]).readlines()
	lista_id = []
	for line in input[3:]:
		text = line.split()
		id = text[4]
		lista_id.append(id[:-1])
	lista_id = list(set(lista_id))
	lista_id.sort()
	handle = open(file[:-5], "rU")
	sequen = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
	handle.close()
	print "Getting sequences..."
	for el in lista_id:
		out_in1.write(">%s\n%s\n" % (el+"/1", str(sequen[el+"1"].seq)))
		out_in2.write(">%s\n%s\n" % (el+"/2", str(sequen[el+"2"].seq)))
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

