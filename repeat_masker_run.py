#! /usr/bin/python

from subprocess import call

library = raw_input("Introduce library name: ")
threads = raw_input("Introduce number of threads: ")

files = open("lista.txt").readlines()

for file in files:
	call("RepeatMasker -par %s -nolow -no_is -engine crossmatch -lib %s %s" % (threads, library, file[:-1]) , shell=True)
