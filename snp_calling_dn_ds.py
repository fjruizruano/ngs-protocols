#!/usr/bin/python

import sys
from subprocess import call

if len(sys.argv) == 1:
    print "\nUsage: snp_calling_dn_ds.py Reference BamFile\n"

try:
    ref = sys.argv[1]
except:
    ref = raw_input("Introduce Reference in FASTA: ")

try:
    bam = sys.argv[2]
except:
    bam = raw_input("Introduce Sorted BAM file: ")

name = bam.split(".")
name = name[0]

# SNP calling with Samtools
print "samtools_1_1 mpileup -ugf %s -C 50 -d 4000 %s | bcftools call -vmO z -o %s" % (ref, bam, name+".vcf.gz")
call("samtools_1_1 mpileup -ugf %s -C 50 -d 4000 %s | bcftools call -vmO z -o %s" % (ref, bam, name+".vcf.gz"), shell=True)

# Index 
print "tabix -p vcf %s" % name+".vcf.gz"
call("tabix -p vcf %s" % name+".vcf.gz", shell=True)

# Filter data
print """bcftools filter -O z -o %s -s LOWQUAL -i'%%QUAL>10' %s""" % (name+"_filt.vcf.gz", name+".vcf.gz")
call("""bcftools filter -O z -o %s -s LOWQUAL -i'%%QUAL>10' %s""" % (name+"_filt.vcf.gz", name+".vcf.gz"), shell=True)

# Index
print "tabix -p vcf %s" % (name+"_filt.vcf.gz")
call("tabix -p vcf %s" % (name+"_filt.vcf.gz"), shell=True)

# Stats
print """bcftools stats -F %s -f "PASS,." -s - %s > %s""" % (ref, name+"_filt.vcf.gz", name+"_filt.vcf.gz.stats")
call("""bcftools stats -F %s -f "PASS,." -s - %s > %s""" % (ref, name+"_filt.vcf.gz", name+"_filt.vcf.gz.stats"), shell=True)
