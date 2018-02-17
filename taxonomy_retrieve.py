#!/usr/bin/python

import sys
from subprocess import call

print "taxonomy_retrieve.py TaxonList"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce Taxon List: ")

li = open(file).readlines()

command = "wget -nv -O tmp_taxon.txt https://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/scientific-name/"

out = open(file+".taxo", "w")

for el in li:
    taxo = "Unknown"
    info = el.split()
    species = info[:2]
    call(command+"\ ".join(species), shell=True)
    tax_file = open("tmp_taxon.txt").readlines()
    for line in tax_file:
        if line.startswith("    \042lineage\042"):
            taxo = line.split(":")

    taxo = taxo[1][2:-4]

    out.write("%s\t%s\n" % (" ".join(species),taxo))
    out.flush()

call("rm tmp_taxon.txt", shell=True)
out.close()
