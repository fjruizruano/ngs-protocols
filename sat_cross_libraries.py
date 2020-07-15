#!/usr/bin/python

from subprocess import call
import sys

print "Usage: sat_cross_libraries.py FastaLibrary RepeatMaskerOutFile SatelliteNamesList"

try:
    fasta = sys.argv[1]
except:
    fasta = raw_input("Introduce Fasta file (reads): ")

try:
    out = sys.argv[2]
except:
    out = raw_input("Introduce RepeatMasker's OUT file: ")

try:
    sats = sys.argv[3]
except:
    sats = raw_input("Introduce list of satellite names: " )

out_prefix = out.split(".")
out_prefix = out_prefix[0]

list_sats = open(sats).readlines()

for sat in list_sats:
    sat = sat[:-1]
    print "\n" + sat
    call("""grep "%s" %s > %s.%s.out""" % (sat,out,out_prefix,sat) , shell=True)

    call("""awk {'print $5'} %s.%s.out | sed 's/\//\134t/g' | awk {'print $1'} | sort -u | awk {'print $1"/1\134n"$1"/2"'} > %s.%s.names""" % (out_prefix,sat,out_prefix,sat), shell=True) 

    call("seqtk subseq %s %s.%s.names > %s.%s.fasta" % (fasta,out_prefix,sat,out_prefix,sat), shell=True)
    call("seqkit sort --by-name %s.%s.fasta > %s.%s.sort.fasta" % (out_prefix,sat,out_prefix,sat), shell=True)
