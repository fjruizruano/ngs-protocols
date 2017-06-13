#!/usr/bin/python

import sys
from numpy import mean,std
from subprocess import call

print "Usage: coverage_graphics.py CoverageFile SamplesFile"

try:
    coverage_file = sys.argv[1]
except:
    coverage_file = raw_input("Introduce coverage file: ")

try:
    samples_file = sys.argv[2]
except:
    samples_file = raw_input("Introduce samples file: ")

coverages = open(coverage_file).readlines()

samples = open(samples_file).readlines()

di_samples = {}
lib_sizes = []
genome_sizes = []

for n in range(0,len(samples)):
    info = samples[n]
    info = info.split()
    if info[2] not in di_samples:
        di_samples[info[2]] = [n]
    else:
        di_samples[info[2]].append(n)
    lib_sizes.append(int(info[3]))
    genome_sizes.append(int(info[4]))

s_norm = open(samples_file+".norm","w")
s_norm.write("".join(coverages[:2]))
for line in coverages[2:]:
    info = line.split()
    normalized = info[0:2]
    for n in range(0,len(samples)):
        normalized.append(str(1.0*genome_sizes[n]*int(info[n+2])/lib_sizes[n]))
    s_norm.write("\t".join(normalized)+"\n")
s_norm.close()

print di_samples

coverages_norm = open(samples_file+".norm").readlines()

genes = {}

for line in coverages[2:]:
    info = line.split()
    main_info = info[1:]
    if info[0] not in genes:
        genes[info[0]] = [main_info]
    else:
        genes[info[0]].append(main_info)

r_script = open("r_script.R","w")
r_script.write("library(ggplot2)\n")
i = 0
for gene in genes:
    i += 1
    str_i = str(i)
    while len(str_i) < 4:
        str_i = "0"+str_i
    print gene
    out = open("tmp_input_%s.txt" % str_i, "w")
    header = ["position"]
    keys = []
    for s in di_samples:
        header.extend((s+"mean",s+"stdev",s+"stdevd",s+"stdevu"))
        keys.append(di_samples[s])
    out.write("\t".join(header))
    out.write("\n")
    data = genes[gene]
    for d in data:
        calcs = [d[0]] # position
        for key in keys:
            join = []
            for number in key:
                join.append(int(d[number+1]))
            media = mean(join)
            stdev = std(join, ddof=1)
#            stdev = std(join)
            calcs.extend((media,stdev,media-stdev,media+stdev))
        out.write("\t".join(str(f) for f in calcs))
        out.write("\n")
    out.close()

    code = """fas2 <- read.table("tmp_input_%s.txt", header=TRUE)\npdf("%s.pdf",height=3)\nggplot(fas2,aes(fas2$position))+geom_line(aes(y=fas2$zbmean,colour="blue"))+geom_line(aes(y=fas2$pbmean,colour="red"))+geom_ribbon(aes(ymin=fas2$zbstdevd,ymax=fas2$zbstdevu), alpha=0.2,fill="red")+geom_ribbon(aes(ymin=fas2$pbstdevd,ymax=fas2$pbstdevu),alpha=0.2,fill="blue")+scale_colour_manual(name="name",labels=c("0B","+B"),values=c("red","blue"))+xlab("Position")+ylab("Number of copies")+ggtitle("%s\n")+theme_bw()+theme(plot.title = element_text(hjust=0.5,size=12))\ndev.off()\n""" % (str_i, str_i, gene)
    r_script.write(code)

r_script.close()

call("Rscript r_script.R", shell=True)
