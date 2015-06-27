#!/usr/bin/python

import sys
from subprocess import call

print "Usage: trinotate_auto.py FastaFile NumberOfThreads DataBase(su) Analysis(xph) [MinimumLenghtCDS]"

try:
    transcripts = sys.argv[1]
except:
    transcripts = raw_input("Introduce FASTA file: ")

try:
    threads = sys.argv[2]
    tt = int(threads)
except:
    threads = raw_input("Intruduce number of threads (integer): ")

try:
    db = sys.argv[3]
except:
    db = raw_input("Introduce databases (s=swissprot, u=uniref90, p=pfam, su, sp, up): ")

try:
    analyses = sys.argv[4]
except:
    analyses = raw_input("Introduce analyses (x=blastx, p=blastp, h=hammer, xp, xh, ph, xph): ")

try:
    cdslen = sys.argv[5]
    tc = int(cdslen)
except:
    tc = "100"

s = "/mnt/disk2/trinotate/swissprot/uniprot_sprot.trinotate_v2.0.pep"
u = "/mnt/disk2/trinotate/uniref90/uniprot_uniref90.trinotate_v2.0.pep"
h = "/mnt/disk2/trinotate/pfam/Pfam-A.hmm"
db_dict = {"s": s, "u":u, "h":h}

if "p" in analyses or "h" in analyses:
    call("TransDecoder.LongOrfs -t %s -m %s" % (transcripts,cdslen), shell=True)
    pep = transcripts + ".transdecoder_dir/longest_orfs.pep"

if "x" in analyses:
    for d in db:
        print "Running BLASTX with " + db_dict[d]
        call("blastx -query %s -db %s -num_threads %s -max_target_seqs 1 -outfmt 6 > %s.%s.blastx.outfmt6" % (transcripts,db_dict[d],threads,transcripts,d) , shell=True)

if "p" in analyses:
    for d in db:
        print "Running BLASTP with " + db_dict[d]
        call("blastp -query %s -db %s -num_threads %s -max_target_seqs 1 -outfmt 6 > %s.%s.blastp.outfmt6" % (pep,db_dict[d],threads,transcripts,d) , shell=True)

if "h" in analyses:
    print "Running HMMER with " + h
    call("hmmscan --cpu %s --domtblout %s.pfam.out %s %s > pfam.log" % (threads,transcripts,h,pep), shell=True)

