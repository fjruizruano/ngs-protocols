#!/usr/bin/python2

import sys
from subprocess import call

print "Usage: gfa2fas.py GfaFile"

try:
    gfa = sys.argv[1]
except:
    gfa = raw_input("Introduce GFA file: ")

gfa_name = gfa.split(".")
gfa_name = gfa_name[:-1]
gfa_name = ".".join(gfa_name)

awk = """awk '/^S/{print ">"$2;print $3}' %s > %s.fasta""" % (gfa, gfa_name)
call(awk, shell=True)

