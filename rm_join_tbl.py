#! /usr/bin/python

files = open("lista_tbl.txt")
outout = open("test.all.tbl", "w")

t = 0
m = 0

for file in files:
        file = open(file[:-1]).readlines()
        total = file[3]
	total = total.split()
	total = int(total[2])

	masked = file[5]
	masked = masked.split()
	masked = int(masked[2])

	t += total
	m += masked

	print str(t) + "\t" + str(m) + "\t" + str(100.0*m/t) + "%"

outout.write("total bases\tmasked bases\tproportion of masked bases\n")
outout.write(str(t) + "\t" + str(m) + "\t" + str(100.0*m/t) + "%")
		
outout.close()

