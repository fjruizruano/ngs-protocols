#!/usr/bin/python

import sys
from numpy import mean,std
from subprocess import call

print "Usage: coverage_graphics.py CoverageFile SamplesFile FastaFile"

try:
    coverage_file = sys.argv[1]
except:
    coverage_file = raw_input("Introduce coverage file: ")

try:
    samples_file = sys.argv[2]
except:
    samples_file = raw_input("Introduce samples file: ")

try:
    fasta_file = sys.argv[3]
except:
    fasta_file = raw_input("Introduce FASTA file: ")

coverages = open(coverage_file).readlines()

samples = open(samples_file).readlines()

di_samples = {}

di_conditions = {}
li_conditions = []
lib_sizes = []
genome_sizes = []

for n in range(0,len(samples)):
    info = samples[n]
    info = info.split()
    cond = info[1].split("_")

    # creating conditions dictionary
    if cond[0] not in di_conditions:
        di_conditions[cond[0]] = [info[1]]
        li_conditions.append(cond[0])
    elif info[1] not in di_conditions[cond[0]]:
        di_conditions[cond[0]].append(info[1])

    # creating samples dictionary
    if info[1] not in di_samples:
        di_samples[info[1]] = [n]
    else:
        di_samples[info[1]].append(n)
    lib_sizes.append(int(info[2]))
    genome_sizes.append(int(info[3]))

#print len(samples)
#print di_samples
#print di_conditions
#print li_conditions

s_norm = open(coverage_file+".norm","w")
s_norm.write("".join(coverages[:2]))
for line in coverages[2:]:
    info = line.split()
    normalized = info[0:2]
    for n in range(0,len(samples)):
        normalized.append(str(1.0*genome_sizes[n]*int(info[n+2])/lib_sizes[n]))
    s_norm.write("\t".join(normalized)+"\n")
s_norm.close()

#print di_samples

coverages_norm = open(coverage_file+".norm").readlines()

genes = {}
li_genes = []

fasta_read = open(fasta_file).readlines()
for line in fasta_read:
    if line.startswith(">"):
        line = line.split()
        li_genes.append(line[0][1:])

for line in coverages_norm[2:]:
    info = line.split()
    main_info = info[1:]
    if info[0] not in genes:
        genes[info[0]] = [main_info]
    else:
        genes[info[0]].append(main_info)

#print genes
#print li_genes

li_genes_corrected = []

out_nf = open("not_found.txt","w")

for gene in li_genes:
    if gene in genes:
        li_genes_corrected.append(gene)
    else:
        out_nf.write("%s\n" % (gene))

out_nf.close()

out_av = open(coverage_file+".av","w")


#Writing header
h = ["Sequence"]
for line in samples:
    l = line.split()
    h.append(l[0])
out_av.write("\t".join(h)+"\n")

print di_samples

for gene in li_genes_corrected:
    data = genes[gene]
    li_cov = []
    for n in range(1,len(samples)+1):
        li_cov.append([])
    for el in data:
        values = el[1:]
        for n in range(0,len(samples)):
            number = values[n]
            li_cov[n].append(float(number))

    li_averages = []

    for el in li_cov:
        average = sum(el)/float(len(el))
        li_averages.append(average)
    li_averages = [str(i) for i in li_averages]
    out_av.write("%s\t%s\n" % (gene,"\t".join(li_averages)))

out_av.close()

r_script = open("r_script.R","w")
r_script.write("library(grid)\nlibrary(gridExtra)\nlibrary(ggplot2)\n")
palette = ["red", "blue", "green3", "black", "cyan", "magenta", "yellow", "gray"]
i = 0
for gene in li_genes_corrected:
    i += 1
    str_i = str(i)
    while len(str_i) < 4:
        str_i = "0"+str_i
    print gene
    out = open("tmp_%s.txt" % str_i, "w")

    #Writing header
    header = ["position"]
    for conditions in li_conditions:
        #selecting samples
        di_selection={}
        for c in di_conditions[conditions]:
            di_selection[c] = di_samples[c]

        for s in di_selection:
            header.extend((s+"_mean",s+"_stdev",s+"_stdevd",s+"_stdevu"))

    out.write("\t".join(header)+"\n")

    #Writing transformed data
    data = genes[gene]
    for d in data: # for each position
        calcs = [d[0]] # position
        #For gDNA or RNA
        for conditions in li_conditions:
            #selecting samples: gdna_zb or gdna_pb
            di_selection={}
            for c in di_conditions[conditions]: 
                di_selection[c] = di_samples[c]
            keys = []
            for s in di_selection:
                keys.append(di_samples[s])

            for key in keys: #1,2 and 3,4
                join = []
                for number in key:
                    join.append(float(d[number+1]))
                media = mean(join)
                stdev = 0
                if len(join) > 1:
                    stdev = std(join, ddof=1)
                calcs.extend((media,stdev,media-stdev,media+stdev))
        out.write("\t".join(str(f) for f in calcs))
        out.write("\n")
    out.close()

    r_script.write("""\nfas2 <- read.table("tmp_%s.txt", header=TRUE)\n""" % (str_i))

    k = 0

    for condition in li_conditions: #gDNA or RNA
        #print condition

        k += 1
        if k == 1:
            title_code = """+labs(title=\042%s\134n\042)""" % gene
        else:
            title_code = ""

        j = -1
        pat = []
        sta = []
        states = di_conditions[condition]
        states_inv = states[::-1]
        #print states
        code = """%s <- ggplot(fas2,aes(fas2$position))""" % (condition)
        color = len(states)
        for s in states_inv:
            #print s
            sta.insert(0,"\042%s\042=\042%s\042" % (str(color),palette[color-1]))
            pat.insert(0,"\042%s\042=\042%s\042" % (str(color),s))
            code = code + """+geom_line(aes(y=fas2$%s_mean,colour="%s"))""" % (s, str(color))
            code = code + """+geom_ribbon(aes(ymin=fas2$%s_stdevd,ymax=fas2$%s_stdevu), alpha=0.2,fill="%s")""" % (s,s,palette[color-1])
            color -= 1

        if condition.startswith("gdna"): # zb or pb
            code = code + """+scale_colour_manual(name="condition",values=c(%s),labels=c(%s))+xlab("Position")+ylab("Number of copies")+theme_bw()%s\n""" % (",".join(sta),",".join(pat),title_code)
            r_script.write(code)

        elif condition.startswith("rna"):
            code = code + """+scale_colour_manual(name="condition",values=c(%s),labels=c(%s))+xlab("Position")+ylab("Expression Level")+theme_bw()%s\n""" % (",".join(sta),",".join(pat),title_code)
            r_script.write(code)
    condit = []
    for condition in li_conditions:
        condit.append("ggplotGrob(%s)" % condition)
    code = """pdf("tmp_%s.pdf", onefile = TRUE)\ngrid.newpage()\ngrid.draw(rbind(%s, size="max"))\ndev.off()""" % (str_i, ",".join(condit))
    r_script.write(code)

r_script.close()

call("Rscript r_script.R", shell=True)

call("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf tmp*pdf", shell=True)
