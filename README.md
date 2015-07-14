ngs-protocols
=============

####Scripts to run several protocols to processing and analyzing of Next-Generation Sequencing data

* FastA.split.pl: Split FASTA files in several subfiles.
* FastQ.split.pl: Split FASTQ files in several subfiles.
* bg_count.py: Generate a table with nucleotide counts from BAM files.
* blat_recursive.py: Parallelize a BLAT run in several threads.
* blat_recursive_hard.py: Parallelize a BLAT run in several threads with hard options.
* bowtie2_recursive.py: Map using Bowtie2 with several libraries consecutively.
* bwa_protocol.py Map using BWA in a single library.
* count_bases_fastq.py: Count number of nucleotides in one o several FASTQ(.GZ) files.
* count_kmer.py: Count occurrences from a list of kmers using Jellyfish.
* count_reads_bam.py: Generate a table with mapped reads counts in several BAM files.
* coverage_seq_bed.py: Count number of mapped nucleotides per reference sequence in BED files.
* coverage_window.py: Count number of mapped nucleotides in a sliding window of defined size.
* cut_seq_unequal.py: Trim sequences from a FASTA file in subsequence of the defined size
