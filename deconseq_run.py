#!/usr/bin/python

import sys, os
from subprocess import call, Popen
from os import listdir
from os.path import isfile, join

print "Usage: deconseq_run.py ListOfFiles Reference Threads"

try:
    files = sys.argv[1]
except:
    files = raw_input("Introduce list of files: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce FASTA reference: ")

try:
    thr = sys.argv[3]
except:
    thr = raw_input("Introduce number of threads")

refp = ref.split(".")
refpoints = refp[0:-1]
refname = ".".join(refpoints)

files = open(files).readlines()

dsdir = "deconseq-standalone-0.4.3"

elements = os.listdir(".")
if dsdir not in elements:
    call("cp -r /usr/local/lib/%s ." % dsdir, shell=True)
    call("mkdir %s/db" % dsdir, shell=True)

os.chdir(dsdir+"/db")
call("ln -sf ../../%s" % ref, shell=True)
call("../bwa64 index -p %s -a is %s" % (refname,ref), shell=True)
os.chdir("../")
conf = open("DeconSeqConfig.pm").readlines()
conf_out = open("tmp_conf.txt", "w")
line1 = " "*21+"%s => {name => \047%s\047,\n" % (refname,refname)
line2 = " "*30+"db => \047%s\047},\n" % (refname)
conf.insert(20, line1+line2)
conf_out.write("".join(conf))
conf_out.close()
call("mv tmp_conf.txt DeconSeqConfig.pm", shell=True)

os.chdir("../")
for n in range(0,len(files)/2):
    file1 = files[n*2][:-1]
    file2 = files[(n*2)+1][:-1]
    ext1 = file1.split(".")
    if ext1[-1] == "gz":
        file1_n = ext1[0:-1]
        file1_n = ".".join(file1_n)
        print "Uncompressing file %s" % file1
        call("seqtk seq %s > %s" % (file1, file1_n), shell=True)
        file1 = file1_n
    ext2 = file2.split(".")
    if ext2[-1] == "gz":
        file2_n = ext2[0:-1]
        file2_n = ".".join(file2_n)
        print "Uncompressing file %s" % file2
        call("seqtk seq %s > %s" % (file2, file2_n), shell=True)
        file2 = file2_n

    os.chdir(dsdir)
    
    filename = file1.split(".")
    filename = filename[0]

    call("ln -sf ../%s ." % file1 , shell=True)
    call("ln -sf ../%s ." % file2 , shell=True)

    call("FastQ.split.pl %s tmp_queries_1 %s" % (file1, thr), shell=True)
    call("FastQ.split.pl %s tmp_queries_2 %s" % (file2, thr), shell=True)

    onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
    splits = []
    for f in onlyfiles:
        if f.startswith("tmp_queries_1") or f.startswith("tmp_queries_2") and f.endswith(".fastq"):
            splits.append(f)
    splits.sort()

    commands = []
    for round in range(0,2):
        commands.append([])

    for n in range(0,len(splits)):
        fq = splits[n]
        com = "perl deconseq.pl -f ./%s -out_dir %s/%s -dbs %s" % (fq, filename, fq, refname)
        rr = n/int(thr)
        commands[rr].append(com)

    print commands

    print "Running DeconSeq"
    for command in commands:
        processes = [Popen(cmd, shell=True) for cmd in command]
        for p in processes:
            p.wait()
    
    

    os.chdir("./%s" % filename)
    for n in range(1,3):
        concat = ["cat"]
        for fq in splits:
            if fq.startswith("tmp_queries_%s" % (str(n))):
                concat.append("%s/*clean*" % (fq))
        call("%s > %s_%s.fastq" % (" ".join(concat), filename[:-2], str(n)), shell=True)
        print concat
    os.chdir("../")

    if ext1[-1] == "gz":
        call("rm %s" % (file1), shell=True)
    if ext2[-1] == "gz":
        call("rm %s" % (file2), shell=True)

    call("rm tmp_queries*.fastq", shell=True)
    call("rm -r %s/tmp_queries*.fastq" % (filename), shell=True)
