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
* cut_seq_unequal.py: Trim sequences from a FASTA file in subsequence of the defined size.
* divnuc_bam.py: Calculate nucleotide diversity per site from BAM files.
* divnuc_plot.py: Calculate nucleotide diversity per window from the output of divnuc_bam.py
* dnapipete_createdb.py: Generate a database compatible with RepeatMasker from the dnaPipeTe
* extract_member_reads_rexp.py: Extract reads in a specific cluster of RepeatExplorer.
* extract_no_seq.py: Extract sequecences from a FASTA file absent in a list.
* extract_reads_blat.py: Extract matching reads in a PSL output from BLAT.
* extract_reads_rm.py: Extract matching reads in a OUT output from RepeatMasker.
* extract_seq.py: Extract sequences from a FASTA file present in a list conserving the order.
* fasta_filter_by_length.py: Filter out sequences from a FASTA file with a size lower than a thereshold.
* fasta_sequence_len.py: Generate a table with the length of each sequence in a FASTA file.
* fastq-combine-pe.py: Extract reads paired reads by ID from two FASTQ files.
* fastq-pe-random.py: Random selection of paired reads from two FASTQ files.
* fastq_edit_ids.py: Edit the ID from FASTQ files to end with the format "@ID/1".
* find_exclusive_kmers.py: Extract exclusive kmers of a library in comparison with other using Jellyfis.
* get_no_blat.py: Extract sequences from a FASTA file absent in a PSL output of BLAT.
* id_rmasker.py: Edit IDs from a FASTA file with a format compatible with RepeatMasker.
* id_rmasker_rexp.py: Edit IDs from a FASTA file of RepeatExplorer contigs compatible with RepeatMasker.
* join_multiple_lists.py: Join the results of two or more lists.
* join_rm_list.py: Join two files with RepatMasker nucleotide counts.
* kimura_window.py: Calculate kimura divergence per window using the RepeatMasker's script.
* kmer_to_fasta.py: Generate a FASTA file from a list of kmers.
* mapping_blat_gs.py: Extract matching reads with BLAT and optionally launch Newbler, RepeatMasker or SSAHA2
* mapping_blat_gs_hard.py: Extract matchin reads with hard options of BLAT and optionally launch Newbler, RepeatMasker or SSAHA2.
* mitobim_run.py: Run MITObim with several protocols.
* mreps_extract.py: Generate a FASTA file with tandem sequences using a MREPS output.
* reduce_bam.py: Filter out unmapped paired reads from a BAM file.
