#! /usr/bin/python

file = raw_input("MREPS output file: ")
tag = raw_input("Introduce tag (six first characters): ")

data = open(file).readlines()

mark = " " + "-"*93 + "\n"
lista = []
check = 0
seq_id = ""
j = -1

out = open(file+".fas", "w")
out_full = open(file+".full.txt", "w")

# para cada linea en el fichero
for line in data:
	j += 1
	l = line.find(tag)

	# almacena el nombre de la sequencia si aparece
	if l != -1:
		seq_id = line[21:-2]
		seq_id = seq_id.split(" ")

	# si comienza la marca, extrae las secuencias hasta la proxima
	if line == mark:
#		out_full.write(seq_id[0]+"\n")
		check +=1
		if check%2 == 1:
			out_full.write(seq_id[0]+"\n")
			k = 0
			lista.append(seq_id[0])
			for i in range(1,100):
				if data[j+i] != mark:
					sequen = data[j+i]
					sequen = sequen.split("\t\t")
					sequen = sequen[-1]
					sequen = sequen.split(" ")
					sequen = sequen[:-1]
					for seq in sequen:
						k += 1
						out.write(">%s_%s\n%s\n" % (seq_id[0], str(k), seq))
				else:
					break

out.close()
out_full.close
