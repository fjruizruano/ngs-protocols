#!/usr/bin/python
import os
from subprocess import call

subfol = os.walk('.').next()[1]

com = "cat "

for num in range(1,len(subfol)+1):
	n = str(num)
	while len(n) < 4:
		n = "0" + n
	com = com + "./dir_CL%s/contigs_CL%s " % (n, num)

com = com + "> out.txt"

print com

call(com, shell=True)
