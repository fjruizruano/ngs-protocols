#!/usr/bin/python

from subprocess import call, Popen, PIPE
from re import compile
import os

mink = raw_input("Input min kmer (odd number): ")
maxk = raw_input("Input max kmer (odd number): ")
file1 = raw_input("Input name file1: ")
#file1 = "greg_1_1.fastq"
file2 = raw_input("Input name file2: ")
#file2 = "greg_1_2.fastq"
name_proj = raw_input("Input project name: ")
cores = raw_input("Input number of cores: ")

splitter = compile("\n") # regla para separar los elementos de la lista
f = open("stats.txt", "a") # crear fichero stats.txt
f.write("kmer_length\tsum\tn\ttrim_n\tmin\tmed\tmean\tmax\tn50\tn50_len\tn90\tn90_len\n") # copiar cabecera en fichero stats.txt
f.close()

for k in range (int(mink),int(maxk)+1):
	if k%2 == 1:
		call("mkdir k%s && mv %s ./k%s/ && mv %s ./k%s/" % (k, file1, k, file2, k), shell=True) # crea directorio del kmer y mueve alli los ficheros de entrada
		os.chdir("./k%s" % k) # se introduce en el directorio del kmer
		call("abyss-pe n=1 c=1 E=0 m=30 q=3 np=%s k=%s v=-v OVERLAP_OPTIONS=\042--no-scaffold\042 SIMPLEGRAPH_OPTIONS=\042--no-scaffold\042 MERGEPATHS_OPTIONS=\042--no-scaffold\042 MERGEPATHS_OPTIONS=\042--greedy\042 mp=\042\042  in=\042%s %s\042 name=%s" % (cores, k, file1, file2, name_proj), shell=True) # ejecuta abyss
		call("mv %s ../ && mv %s ../" % (file1, file2), shell=True) # desplaza los ficheros de entrada a la carpeta original
		os.chdir("../") # devuelve al directorio de partida
		(stdout,stderr) = Popen("assemstats.py 100 ./k%s/%s-contigs.fa" % (k, name_proj), shell=True, stdout=PIPE).communicate() # coger salida assemstats
		stdout = splitter.split(stdout)	# de cadena a lista segun la regla
		f = open("stats.txt", "a") # crear fichero stats.txt
		f.write("%s\t" % k + "".join(stdout[1]) + "\n") # copiar la linea de la estadistica en el fichero stats.txt
		f.close()
