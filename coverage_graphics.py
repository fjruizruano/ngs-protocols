#!/usr/bin/python

import sys
from numpy import mean,std
from subprocess import call

print "Usage: coverage_graphics.py CoverageFile SamplesFile FastaFile PDF/SVG/NOPLOT [SNPsFile]" 

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

try:
    plot_question = sys.argv[4]
except:
    plot_question = raw_input("Do you want to generate plots [PDF/SVG/NOPLOT]: ")

snps_question = 0
try:
    snp_file = sys.argv[5]
    snp_data = open(snp_file).readlines()
    snps_question = 1
except:
    print "You didn't indicate SNPs file. Ignoring."
    pass

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
    lib_sizes.append(float(info[2]))
    genome_sizes.append(float(info[3]))

#print len(samples)
#print di_samples
#print di_conditions
#print li_conditions

s_norm = open(coverage_file+".norm","w")
s_norm.write("".join(coverages[:1]))
for line in coverages[1:]:
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
di_cds = {} 

fasta_read = open(fasta_file).readlines()
for line in fasta_read:
    if line.startswith(">"):
        line = line.split(" ")
        li_genes.append(line[0][1:])
        di_cds[line[0][1:]] = line[1]

for line in coverages_norm[1:]:
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

if snps_question == 1:
  snp_data = open(snp_file).readlines()
  snp_dict = {}

  if type(snp_data) is list:
    for line in snp_data:
        line = line.split()
        a = line[0]
        b = line[1]
        if a in snp_dict:
            snp_dict[a].append(b)
        else:
            snp_dict[a] = [b]

  #print snp_dict

if plot_question == "PDF" or plot_question == "SVG":
  r_script = open("r_script.R","w")
  r_script.write("library(gridExtra)\nlibrary(ggplot2)\nlibrary(egg)\n")
  palette = ["blue", "red", "green3", "black", "cyan", "magenta", "yellow", "gray"]
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


      if snps_question == 1:

        snp_pos = 0
        if len(snp_dict) > 0:
          try:
            snp_pos = snp_dict[gene]

            aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")"""
            bb = """+geom_vline(xintercept=c(%s),linetype="solid")""" % ",".join(snp_pos)
            cc = """+theme_bw()+theme(axis.title.x=element_blank(),axis.text.x=element_blank())"""
            r_script.write(aa+bb+cc+"\n")
          except:
            aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")"""
            cc = """+theme_bw()+theme(axis.title.x=element_blank(),axis.text.x=element_blank())"""
            r_script.write(aa+cc+"\n")

#         print snp_dict

      k = 0

      cds = di_cds[gene]
      cds = cds.replace("-",",")
  
      for condition in li_conditions: #gDNA or RNA
          #print condition
  
          k += 1
          if k == 1:
              title_code = """+labs(title=\042%s\134n\042)""" % gene
          else:
              title_code = ""
  
  
          position_lab = ""
          theme_lab = """axis.title.x=element_blank(),axis.text.x=element_blank()"""
          if k == len(li_conditions):
              position_lab = """+xlab("Position")"""
              theme_lab = ""
  
          j = -1
          pat = []
          sta = []
          states = di_conditions[condition]
          states_inv = states[::-1]
          #print states
          code = """%s <- ggplot(fas2,aes(fas2$position))+geom_vline(xintercept=c(%s),linetype="dotted")""" % (condition,cds)
          color = len(states)
          for s in states_inv:
              #print s
              subcond = s.split("_")
              subcond = subcond[1]
              sta.insert(0,"\042%s\042=\042%s\042" % (str(color),palette[color-1]))
              pat.insert(0,"\042%s\042=\042%s\042" % (str(color),subcond))
              code = code + """+geom_line(aes(y=fas2$%s_mean,colour="%s"))""" % (s, str(color))
              code = code + """+geom_ribbon(aes(ymin=fas2$%s_stdevd,ymax=fas2$%s_stdevu), alpha=0.2,fill="%s")""" % (s,s,palette[color-1])
              color -= 1
  
          if condition.startswith("gDNA"): # zb or pb
              code = code + """+scale_colour_manual(name="%s",values=c(%s),labels=c(%s))%s+ylab("Number of copies")+theme_bw()+theme(%s)%s\n""" % (condition,",".join(sta),",".join(pat),position_lab,theme_lab,title_code)
              r_script.write(code)
  
          elif condition.startswith("RNA"):
              code = code + """+scale_colour_manual(name="%s",values=c(%s),labels=c(%s))%s+ylab("Reads per million")+theme_bw()+theme(%s)%s\n""" % (condition,",".join(sta),",".join(pat),position_lab,theme_lab,title_code)
              r_script.write(code)
      condit = []
      condit_len = []
      for condition in li_conditions:
          condit.append("%s" % condition)
          condit_len.append(2)

      if snps_question == 1:
        if len(snp_dict) > 0:
          search_gdna = [s for s in condit if "gDNA" in s]
          ind = condit.index(search_gdna[-1])
          ind = ind+1
          condit.insert(ind,"SNPS")
          condit_len.insert(ind,0.5)
      condit_len_str = [str(x) for x in condit_len]
      condit_len_sum = sum(condit_len)
      code = """pdf("tmp_%s.pdf",height=%s,onefile=FALSE)\nggarrange(%s,heights=c(%s),ncol=1)\ndev.off()\n""" % (str_i,str(condit_len_sum), ",".join(condit), ",".join(condit_len_str))
      r_script.write(code)

      if plot_question == "SVG":
          code2 = """svg("tmp_%s.svg",height=%s,onefile=FALSE)\nggarrange(%s,heights=c(%s),ncol=1)\ndev.off()\n""" % (str_i,str(condit_len_sum),",".join(condit), ",".join(condit_len_str))
          r_script.write(code2)
  
  r_script.close()
  
  call("Rscript r_script.R", shell=True)
  
  call("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf tmp*pdf", shell=True)
