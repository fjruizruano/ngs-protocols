#!/usr/bin/python

import sys
from subprocess import call

print "\nUsage: bwa_protocol.py ListOfReads Reference Threads [noreduce/reduce]\n"

try:
    data = sys.argv[1]
except:
    data = raw_input("List of reads: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("FASTA reference file: ")

try: 
    threads = sys.argv[3]
except:
    threads = raw_input("Number of threads: ")

try:
    reduce = sys.argv[4]
except:
    reduce = raw_input("Reduce or not reduce: ")

files = open(data).readlines()
l_files = []
for f in range(0,(len(files)/2)):
    l_files.append([files[f*2][:-1],files[(f*2)+1][:-1]])

ref_name = ref.split(".")
ref_name = ".".join(ref_name[:-1])

try:
	open(ref+".pac")
	open(ref+".ann")
	open(ref+".amb")
	open(ref+".bwt")
	open(ref+".sa")
except:
	call("bwa index -a bwtsw %s" % ref, shell=True)

try:
	open(ref+".fai")
except:
	call("samtools faidx %s" % ref, shell=True)

try:
	open(ref_name+".dict")
except:

	call("picard CreateSequenceDictionary R=%s O=%s" % (ref, ref_name+".dict"), shell=True)


for pair in l_files:
    name = pair[0]
    name = name.split(".")
    name = name[0][:-2]

    # map with BWA
#    read_group = "\047@RG\134tID:group1\134tSM:sample1\134tPL:illumina\134tLB:lib1\134tPU:unit1\047"
#    call("bwa mem -M -R %s -t %s %s %s %s > %s" % (read_group, threads, ref, pair[0], pair[1], name+".sam"), shell=True)

    # sort BAM
#    print "picard SortSam INPUT=%s.sam OUTPUT=%s_sort.bam SORT_ORDER=coordinate" % (name,name)
#    call("picard SortSam INPUT=%s.sam OUTPUT=%s_sort.bam SORT_ORDER=coordinate" % (name,name), shell=True)

    # mark duplicates
#    call("picard MarkDuplicates INPUT=%s_sort.bam OUTPUT=%s_sort_md.bam METRICS_FILE=%s_metrics.txt" % (name,name,name), shell=True)

    # index BAM
#    call("picard BuildBamIndex INPUT=%s_sort_md.bam" % (name), shell=True)

    # realignment
    call("gatk -T RealignerTargetCreator -R %s -I %s_sort_md.bam -o %s_targets.list " % (ref,name,name), shell=True)
    call("gatk -T IndelRealigner -R %s -I %s_sort_md.bam -targetIntervals %s_targets.list -o %s_realignment.bam" % (ref,name,name,name), shell=True)

    # call variants
    call("gatk -T HaplotypeCaller -R %s -I %s_realignment.bam --genotyping_mode DISCOVERY -stand_emit_conf 10 -stand_call_conf 30 -o %s.vcf" % (ref,name,name), shell=True)



#    if reduce == "reduce":
#        call("reduce_bam.py %s_sort.bam && rm %s_sort.bam" % (name, name), shell=True)


#########
#    call("bwa aln -t%s %s %s > read1.sai" % (threads, ref, pair[0]), shell=True)
#    call("bwa aln -t%s %s %s > read2.sai" % (threads, ref, pair[1]), shell=True)
#    call("bwa sampe -s -r \042@RG\tID:1\tLB:1\tSM:1\042 %s read1.sai read2.sai %s %s | samtools view -bS - > %s_fastq.bam" % (ref, pair[0], pair[1], name), shell=True)
#    call("rm read1.sai read2.sai", shell=True)
#    call("samtools sort %s_fastq.bam %s_sort" % (name, name), shell=True)
#    call("rm %s_fastq.bam" % (name), shell=True)
#    call("samtools flagstat %s_sort.bam > %s_sort.flagstat" % (name, name), shell=True)
