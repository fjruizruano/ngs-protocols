#! /usr/bin/python

from subprocess import call
from Bio import AlignIO
import sys

print "massive_phylogeny_raxml_support.py FastaFile NumberSearches NumberBootstrap NumberThreads Name"

try:
    file = sys.argv[1]
except:
    file = raw_input("FASTA file name: ")

try:
    trees = sys.argv[2]
except:
    trees = raw_input("Number of searches: ")

try:
    bootstrap = sys.argv[3]
except:
    bootstrap = raw_input("Number of bootstrap: ")

try:
    threads = sys.argv[4]
except:
    threads = raw_input("Number of threads: ")

try:
    name = sys.argv[5]
except:
    name = raw_input("Introduce_number: ")

AlignIO.convert(file, "fasta", file+".phy", "phylip-relaxed")

file_phy = file + ".phy"

try:
    print "raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -# %s -s %s -n run1" % (threads, trees, file_phy)
    call("raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -# %s -s %s -n run1" % (threads, trees, file_phy), shell=True)
except:
    print "IT IS NOT GOOD. PLEASE, CHECK YOUR INPUT FILE(S)"
    sys.exit()
		
call("raxmlHPC-PTHREADS-AVX -T %s -m GTRCAT -p 12345 -b 12345 -# %s -s %s -n run2" % (threads, bootstrap, file_phy), shell=True)

try:
	call("raxmlHPC -m GTRCAT -p 12345 -f b -t RAxML_bestTree.run1 -z RAxML_bootstrap.run2 -n %s.run3" % (name), shell=True)
	call("rm *.run1*", shell=True)
	call("rm *.run2*", shell=True)
	print "AND... HERE WE ARE!"
except:
	print "SOMETHING HAS GONE BAD. PLEASE, CHECK YOUR INPUT FILE(S)"
	sys.exit()
