#!/usr/bin/python

import sys
from subprocess import call

print "Usage: trinotate_auto.py FastaFile NumberOfThreads Analyses(xph) DataBase(su) [MinimumLenghtCDS]"

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
    analyses = sys.argv[3]
except:
    analyses = raw_input("Introduce analyses (x=blastx, p=blastp, h=hammer, xp, xh, ph, xph): ")

try:
    db = sys.argv[4]
except:
    if "h" not in analyses:
        db = raw_input("Introduce databases (s=swissprot, u=uniref90, su): ")
    else:
        pass

try:
    cdslen = sys.argv[5]
    tc = int(cdslen)
except:
    tc = "100"

tex = "/usr/local/lib/Trinotate-2.0.2/Trinotate"
tdb = "/mnt/disk2/trinotate/trinotate_db/Trinotate.sqlite.gz"
tgt = "/usr/local/lib/trinityrnaseq-2.0.6/util/support_scripts/get_Trinity_gene_to_trans_map.pl"

s = "/mnt/disk2/trinotate/swissprot/uniprot_sprot.trinotate_v2.0.pep"
u = "/mnt/disk2/trinotate/uniref90/uniprot_uniref90.trinotate_v2.0.pep"
h = "/mnt/disk2/trinotate/pfam/Pfam-A.hmm"
db_dict = {"s": s, "u":u, "h":h}

try:
    ttt = open("Trinotate.sqlite")
except:
    print "\nPreparing Trinotate DB"
    call("gunzip -c %s > Trinotate.sqlite" % (tdb), shell=True)
    call("%s %s > %s.gene_trans_map" % (tgt, transcripts, transcripts), shell=True)
pep = transcripts + ".transdecoder_dir/longest_orfs.pep"
try:
    ttt = open(pep)
except:
    call("TransDecoder.LongOrfs -t %s -m %s" % (transcripts,cdslen), shell=True)
call("%s Trinotate.sqlite init --gene_trans_map %s.gene_trans_map --transcript_fasta %s --transdecoder_pep %s" % (tex, transcripts, transcripts, pep), shell=True)

if "x" in analyses:
    for d in db:
        print "Running BLASTX with %s\n" % db_dict[d]
        outfile = "%s.%s.blastx.outfmt6" % (transcripts,d)
        call("blastx -query %s -db %s -num_threads %s -max_target_seqs 1 -outfmt 6 > %s" % (transcripts,db_dict[d],threads,outfile) , shell=True)
        if d == "s":
            call("%s Trinotate.sqlite LOAD_swissprot_blastx %s" % (tex,outfile), shell=True)
        elif d == "u":
            call("%s Trinotate.sqlite LOAD_trembl_blastx %s" % (tex,outfile), shell=True)

if "p" in analyses:
    for d in db:
        print "Running BLASTP with %s\n" % db_dict[d]
        outfile = "%s.%s.blastp.outfmt6" % (transcripts,d)
        call("blastp -query %s -db %s -num_threads %s -max_target_seqs 1 -outfmt 6 > %s" % (pep,db_dict[d],threads,outfile), shell=True)
        if d == "s":
            call("%s Trinotate.sqlite LOAD_swissprot_blastp %s" % (tex,outfile), shell=True)
        elif d == "u":
            call("%s Trinotate.sqlite LOAD_trembl_blastp %s" % (tex,outfile), shell=True)

if "h" in analyses:
    print "Running HMMER with " + h
    call("hmmscan --cpu %s --domtblout %s.pfam.out %s %s > pfam.log" % (threads,transcripts,h,pep), shell=True)
    call("%s Trinotate.sqlite LOAD_pfam %s.pfam.out" % (tex, transcripts), shell=True)

call("%s Trinotate.sqlite report > %s.annot.xls" % (tex,transcripts), shell=True)

