#!/usr/bin/python

import sys
from Bio import SeqIO
from subprocess import call

print "\nUsage: kimura_window.py reads.fa reference.fa windowsize step threads\n"

try:
    reads = sys.argv[1]
except:
    reads = raw_input("Introduce reads file: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce reference file: ")

try:
    window = sys.argv[3]
except:
    window = raw_input("Introduce window size: ")

try:
    step = sys.argv[4]
except:
    step = raw_input("Introduce step_size: ")

try:
    threads = sys.argv[5]
except:
    threads = raw_input("Introduce number of threads: ")

def RunRM(ref,reads,threads):
    call("RepeatMasker -pa %s -s -a -nolow -no_is -lib %s %s" % (threads, ref, reads), shell=True)
def GetDIV(reads):
    call("calcDivergenceFromAlign.pl -s %s %s" % (reads+".divsum",reads+".align"), shell=True)
    file = open(reads+".divsum").readlines()
    data = file[7]
    data = data.split()
    data = data[3]
    return data

reference = SeqIO.parse(open(ref),"fasta")
ref_seq = ""
for s in reference:
    ref_seq = s.seq
step = int(step)
window = int(window)
list_div = []
log_file = open("log_"+reads,"w")
log_file.close()

for n in range(0,(len(ref_seq)-window+step)/step):
    sequence = ref_seq[n*step:(n*step)+window]
    seq_file = open(ref+".tmp", "w")
    seq_file.write(">tmp\n%s\n" % sequence)
    seq_file.close()
    RunRM(ref+".tmp",reads,threads)
    x = GetDIV(reads)
    list_div.append(x)
    call("rm %s.tmp" % ref, shell=True)
    call("rm %s.*" % reads, shell=True)
    log_file = open("log_"+reads,"a")
    log_file.write("File number %s of %s: %s\n" % (str(n+1), str((len(ref_seq)-window+window)/step), x))
    log_file.close()

w = open(reads+".divergence", "w")
w.write("\n".join(list_div))
w.close()

log_file.close()
