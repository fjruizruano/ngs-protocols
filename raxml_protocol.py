#! /usr/bin/python

from subprocess import call
from Bio import AlignIO
import os

file = raw_input("FASTA file name: ")
part_file = raw_input("Partition file for RAxML (empty does not use partitions): ")
threads = raw_input("Number of threads: ")
trees = raw_input("Number of searches: ")
bootstrap = raw_input("Number of bootstrap: ")

call("mkdir raxml", shell=True)
os.chdir("raxml")

AlignIO.convert("../"+file, "fasta", file+".phy", "phylip-relaxed")

file_phy = file + ".phy"

if part_file == "": # a different RAxML line if there is partition file or not.
	try:
		print "raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -# %s -s %s -n run1" % (threads, trees, file_phy)
		call("raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -# %s -s %s -n run1" % (threads, trees, file_phy), shell=True)
	except:
		print "IT IS NOT GOOD. PLEASE, CHECK YOUR INPUT FILE(S)"
		sys.exit()
else:
	try:
		print "raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -q ../%s -# %s -s %s -n run1" % (threads, part_file, trees, file_phy)
		call("raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -q ../%s -# %s -s %s -n run1" % (threads, part_file, trees, file_phy), shell=True)
	except:
		print "IT IS NOT GOOD. PLEASE, CHECK YOUR INPUT FILE(S)"
		sys.exit()

call("raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -b 12345 -# %s -s %s -n run2" % (threads, bootstrap, file_phy), shell=True)

try:
	call("raxmlHPC -m GTRCAT -p 12345 -f b -t RAxML_bestTree.run1 -z RAxML_bootstrap.run2 -n run3 ", shell=True)
	print "AND... HERE WE ARE!"
except:
	print "SOMETHING HAS GONE BAD. PLEASE, CHECK YOUR INPUT FILE(S)"
	sys.exit()
