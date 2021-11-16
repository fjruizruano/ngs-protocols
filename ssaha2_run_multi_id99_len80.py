#!/usr/bin/python

import sys
from subprocess import call, Popen
from commands import getstatusoutput
from os import listdir
from os.path import isfile, join

print "Usage: ssaha2_run.py ListOfFiles Reference Threads"

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

try:
    test = open(refname+".head")
    test = open(refname+".body")
    test = open(refname+".size")
    test = open(refname+".name")
    test = open(refname+".base")
except:
    call("ssaha2Build -solexa -save %s %s" % (refname, ref), shell=True)

try:
    test = open(ref+".fai")
except:
    call("samtools faidx %s" % (ref), shell=True)

files = open(files).readlines()

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

    print "Splitting FASTQ files"
    getpre = open(file1)
    getpre = getpre.readline()
    getpre = getpre.split(":")
    n_reads = getstatusoutput("grep -c \042%s\042 %s" % (getpre[0], file1))
    n_reads = int(n_reads[1])
    n_rounds = (n_reads/20000000)+1
#    n_rounds = (n_reads/500000)+1
    n_splits = n_rounds*int(thr)
    print n_splits

    call("FastQ.split.pl %s tmp_queries_1 %s" % (file1, str(n_splits)), shell=True)
    call("FastQ.split.pl %s tmp_queries_2 %s" % (file2, str(n_splits)), shell=True)

    onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
    splits = []
    for f in onlyfiles:
        if f.startswith("tmp_queries_1") and f.endswith(".fastq"):
            splits.append(f)
    splits.sort()

    commands = []
    for round in range(0,n_rounds):
        commands.append([])
    
    for n in range(0,len(splits)):
        fq_one = splits[n]
        fq_two = fq_one.replace("tmp_queries_1", "tmp_queries_2")
        com = "ssaha2 -solexa -pair 20,400 -score 80 -identity 99 -output sam -outfile %s -best 1 -save %s %s %s" % (fq_one+".sam",refname,fq_one,fq_two)
        rr = n/int(thr)
        commands[rr].append(com)

    print "Running SSAHA2"
    for command in commands:
        processes = [Popen(cmd, shell=True) for cmd in command]
        for p in processes:
            p.wait()
    if ext1[-1] == "gz":
        call("rm %s" % (file1), shell=True)
    if ext2[-1] == "gz":
        call("rm %s" % (file2), shell=True)
    call("rm tmp_queries*.fastq", shell=True)
    call("cat *sam > all.sam", shell=True)
    call("rm tmp_queries*.sam", shell=True)

    print "Generating BAM file"
    call("samtools view -F 4 -bt %s.fai %s > %s" % (ref,"all.sam",ext1[0]+".bam"), shell=True)
    call("rm all.sam", shell=True)
    call("samtools sort -T aln.sorted %s -o %s" % (ext1[0]+".bam", ext1[0]+"_mapped.bam"), shell=True)
    call("rm %s" % (ext1[0]+".bam"), shell=True)
    call("samtools index %s" % (ext1[0]+"_mapped.bam"), shell=True)

#    print "Reducing BAM file"
#    call("reduce_bam.py %s" % (file1+".sort.bam"), shell=True)
#    call("rm %s" % (file1+".sort.bam"), shell=True)

call("rm %s" % refname+".head "+refname+".body "+refname+".size "+refname+".name "+refname+".base", shell=True)
