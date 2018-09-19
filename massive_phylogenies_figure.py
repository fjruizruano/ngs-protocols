#!/usr/bin/python

from Bio import Phylo
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import sys

print "massive_phylogeny_figure.py NewickList [Outgroup]"

try:
    lista = sys.argv[1]
except:
    lista = raw_input("Introduce List of Newick files: ")

try:
    outgroup = sys.argv[2]
except:
    outgroup = raw_input("Introduce outgroup name (optioal):")

newicks = open(lista).readlines()

for newick in newicks:
    newick = newick[:-1]
    tree = Phylo.read(newick,"newick")
    og = ""
#    tree.root_with_outgroup({"name": ""})
    if outgroup is not "":
        for clade in tree.find_clades():
            clade = str(clade)
            if clade.find(outgroup) != -1:
                og = clade
                tree.root_with_outgroup({"name": og})

    tree.ladderize()
    #Phylo.draw_ascii(tree)
    Phylo.draw(tree, do_show=False)
    pylab.axis("off")
    plt.suptitle(newick, fontsize=20)
    pylab.savefig(newick+".pdf",format='pdf', bbox_inches='tight', dpi=300)

