#!/usr/bin/python

import sys
from numpy import mean,std,var
from subprocess import call

print "Usage: coverage_graphics.py CoverageFile SamplesFile CoordinatesFile PDF/SVG/NOPLOT [SNPsFile]" 

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
    fasta_file = raw_input("Introduce Coordinates file: ")

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
di_primers = {}
di_highlow = {}

fasta_read = open(fasta_file).readlines()
for line in fasta_read:
#    if line.startswith(">"):
        line = line[:-1]
        line = line.split("\t")
        li_genes.append(line[0])
        if line[1] != "":
            di_cds[line[0]] = line[1]
        if line[2] != "":
            di_primers[line[0]] = line[2]
        if line[3] != "":
            di_highlow[line[0]] = line[3]

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
out_av_high = open(coverage_file+".av.high","w")
out_var = open(coverage_file+".var","w")


#Writing header
h = []
for line in samples:
    l = line.split()
    h.append(l[0])
out_var.write("\t")
out_var.write("\t\t\t\t".join(h)+"\n")
asvc = ["Av","SD","Var","CV"]
asvc = asvc*len(samples)
out_var.write("Sequence\t"+"\t".join(asvc)+"\n")

out_av.write("Sequence\t"+"\t".join(h)+"\n")
out_av_high.write("Sequence\t"+"\t".join(h)+"\n")

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
    li_av = []
    for el in li_cov:
        average = mean(el)
        stdev = std(el, ddof=1)
        vari = var(el)
        try:
          coefvar = float(stdev)/float(average)
        except:
          coefvar = float(0)
        li_averages.append(average)
        li_av.append(average)
        li_averages.append(stdev)
        li_averages.append(vari)
        li_averages.append(coefvar)

    li_averages = [str(i) for i in li_averages]
    li_av = [str(i) for i in li_av]
    out_var.write("%s\t%s\n" % (gene,"\t".join(li_averages)))
    out_av.write("%s\t%s\n" % (gene,"\t".join(li_av)))

    if gene not in di_highlow:
        out_av_high.write("%s\t%s\n" % (gene,"\t".join(li_av)))

    if gene in di_highlow:
      coords = di_highlow[gene]
      coords = coords.split(",")

      hi_coords = []
      for coord in coords:
          coord = coord.split("-")
          hi_coords.append([int(coord[0]),int(coord[1])])
      hi_first = hi_coords[0][0]
      hi_last = hi_coords[-1][-1]
      lo_coords = []
      if len(hi_coords) > 1:
          for i in range(0,len(hi_coords)-1):
              one = hi_coords[i]
              two = hi_coords[i+1]
              lo_coords.append([one[-1]+1,two[0]-1])
              
      if hi_first > 1:
          lo_coords.insert(0,[1,hi_first-1])
      if hi_last < len(el):
          lo_coords.append([hi_last+1,len(el)])

      li_highav = []
      li_lowav = []
      li_hav = []
      li_lav = []

      for el in li_cov:
        li_high = []
        li_low = []
        for hi in hi_coords:
          b = hi[0]-1
          e = hi[1]
          li_high.extend(el[b:e])

        for lo in lo_coords:
          b = lo[0]-1
          e = lo[1]
          li_low.extend(el[b:e])

        average = mean(li_high)
        stdev = std(li_high, ddof=1)
        vari = var(li_high)
        try:
          coefvar = float(stdev)/float(average)
        except:
          coefvar = float(0)
        li_highav.append(average)
        li_hav.append(average)
        li_highav.append(stdev)
        li_highav.append(vari)
        li_highav.append(coefvar)

        average = mean(li_low)
        stdev = std(li_low, ddof=1)
        vari = var(li_low)
        try:
          coefvar = float(stdev)/float(average)
        except:
          coefvar = float(0)
        li_lowav.append(average)
        li_lav.append(average)
        li_lowav.append(stdev)
        li_lowav.append(vari)
        li_lowav.append(coefvar)

      li_lowav = [str(i) for i in li_lowav]
      out_var.write("LOW_%s\t%s\n" % (gene,"\t".join(li_lowav)))
      li_highav = [str(i) for i in li_highav]
      out_var.write("HIGH_%s\t%s\n" % (gene,"\t".join(li_highav)))

      li_lav = [str(i) for i in li_lav]
      out_av.write("LOW_%s\t%s\n" % (gene,"\t".join(li_lav)))
      li_hav = [str(i) for i in li_hav]
      out_av.write("HIGH_%s\t%s\n" % (gene,"\t".join(li_hav)))

      out_av_high.write("HIGH_%s\t%s\n" % (gene,"\t".join(li_hav)))

out_av.close()
out_av_high.close()
out_var.close()

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

  trunc_sum = open("trunc_sum.txt", "w")
  trunc_sum.write("Sequence\tTotal PB High\tTotal nt\tProportion\tTotal PB High CDS\tTotal nt CDS\tProportion CDS\n")

  i = 0

  for gene in li_genes_corrected:
      i += 1
      str_i = str(i)
      while len(str_i) < 4:
          str_i = "0"+str_i
      print gene
      out = open("tmp_%s.txt" % str_i, "w")
 
      zb_trunc = -1
      pb_trunc = -1

      #Writing header
      header = ["position"]
      for conditions in li_conditions:
          #selecting samples
          di_selection={}
          for c in di_conditions[conditions]:
              di_selection[c] = di_samples[c]

          n = 0
          for s in di_selection:
              header.extend((s+"_mean",s+"_stdev",s+"_stdevd",s+"_stdevu"))

              kind_of_sample = s.split("_")
              if kind_of_sample[1].startswith("zzz"):
                  zb_trunc = 1+4*n
              elif kind_of_sample[1].startswith("ppp"):
                  pb_trunc = 1+4*n
              n+=1
  
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

      out_trunc = open("trunc_%s.txt" % str_i, "w")

      get_tmp = open("tmp_%s.txt" % str_i).readlines()

      trunc_hdr = get_tmp[0]
      t = trunc_hdr.split()
      out_trunc.write("%s\t%s\t%s\tpb>zb\tCDS\n" % (t[0],t[zb_trunc],t[pb_trunc]))

      nt_count = 0 # total nt counter
      hi_count = 0 # high cov plusb counter
      nt_count_cds = 0 # total nt counter CDS
      hi_count_cds = 0 # high cov plusb counter CDS

      try:
          cds_interval = di_cds[gene]
          cds_interval = cds_interval.split("-")
          cds_begin = int(cds_interval[0])
          cds_end = int(cds_interval[1])
      except:
          cds_begin = 0
          cds_end = 0

      for temp in get_tmp[1:]:
          nt_count += 1
          t = temp.split()
          zb_num = t[zb_trunc]
          pb_num = t[pb_trunc]
          compar = "False"
          cds_bool = "False"
          if int(t[0]) in range(cds_begin,1+cds_end):
              nt_count_cds += 1
          if float(pb_num) > float(zb_num):
              compar = "True"
              hi_count += 1
              if int(t[0]) in range(cds_begin,1+cds_end):
                  hi_count_cds += 1
                  cds_bool = "True"

          # write position, zzz, ppp, pb>zb
          out_trunc.write("%s\t%s\t%s\t%s\t%s\n" % (t[0],t[zb_trunc],t[pb_trunc],compar,cds_bool))

      out_trunc.close()

      prop = 1.0*hi_count/nt_count
      try:
          prop_cds = 1.0*hi_count_cds/nt_count_cds
      except:
          prop_cds = "--"

#      print str(hi_count) + "/" + str(nt_count)
#      print str(hi_count_cds) + "/" + str(nt_count_cds)

      trunc_sum.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (gene,str(hi_count),str(nt_count),str(prop),str(hi_count_cds),str(nt_count_cds),str(prop_cds)))

      r_script.write("""\nfas2 <- read.table("tmp_%s.txt", header=TRUE)\n""" % (str_i))

      cds_code = ""
      if gene in di_cds:
          cds = di_cds[gene]
          cds = cds.replace("-",",")
          cds_code = """+geom_vline(xintercept=c(%s),linetype="dotted")""" % (cds)

      primer_code = ""
      if gene in di_primers:
          primers = di_primers[gene]
          primers = primers.split(",")
          for p in primers:
              p = p.split("-")
              b = p[0]
              e = p[1]
              primer_code += """+annotate("rect",xmin=%s,xmax=%s,ymin=-Inf,ymax=Inf,alpha=0.1)""" % (str(b), str(e))

      if snps_question == 1:

        snp_pos = 0
        if len(snp_dict) > 0:
          try:
            snp_pos = snp_dict[gene]

 #           aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")%s%s""" % (primer_code,cds_code)
            aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")"""
            bb = """+geom_vline(xintercept=c(%s),linetype="solid")""" % ",".join(snp_pos)
            cc = """+theme_bw()+theme(axis.title.x=element_blank(),axis.text.x=element_blank())"""
            r_script.write(aa+bb+cc+"\n")
          except:
#            aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")%s%s""" % (primer_code,cds_code)
            aa = """SNPS <- ggplot(fas2,aes(fas2$position))+geom_blank()+ylab("SNPs")"""
            cc = """+theme_bw()+theme(axis.title.x=element_blank(),axis.text.x=element_blank())"""
            r_script.write(aa+cc+"\n")

#         print snp_dict

      k = 0

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
          code = """%s <- ggplot(fas2,aes(fas2$position))%s%s""" % (condition,primer_code,cds_code)

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

  trunc_sum.close()
  
  call("Rscript r_script.R", shell=True)
  
  call("gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf tmp*pdf", shell=True)
