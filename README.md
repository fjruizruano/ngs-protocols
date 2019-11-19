ngs-protocols
=============

####Scripts to run several protocols to processing and analyzing of Next-Generation Sequencing data

* FastA.split.pl: Split FASTA files in several subfiles.
* FastQ.split.pl: Split FASTQ files in several subfiles.
* alignment_copy_paste.py: Cut alignment from the left until a position and paste to the right. 
* annot_to_rexp.py: Annotate RepeatExplorer's contigs following a list.
* bam_consensus.py: Get majority consensus sequences for BAM files.
* bam_coverage_join.py: Generate a table of coverage along the contigs in several BAM files.
* bam_var_join.py: Generate a variation table using several BAM files.
* bg_count.py: Generate a table with nucleotide counts from BAM files.
* blat_recursive.py: Parallelize a BLAT run in several threads.
* blat_recursive_hard.py: Parallelize a BLAT run in several threads with hard options.
* bowtie2_recursive.py: Map using Bowtie2 with several libraries consecutively.
* bwa_protocol.py: Map using BWA in a single library.
* cd_hit_filter_size.py: Filter out sequences from small CD-HIT clusters.
* count_acgtn.py: Count number of A, C, G, T and N in a multifasta file.
* count_bases_fastq.py: Count number of nucleotides in one o several FASTQ(.GZ) files.
* count_kmer.py: Count occurrences from a list of kmers using Jellyfish.
* count_reads_bam.py: Generate a table with mapped reads counts in several BAM files.
* coverage_graphics.py: Generate graphics using the ouput from bam_coverage_join.py and a samples file.
* coverage_graphics_coord.py: A complex version of coverage_graphics.py.
* coverage_seq_bed.py: Count number of mapped nucleotides per reference sequence in BED files.
* coverage_window.py: Count number of mapped nucleotides in a sliding window of defined size.
* cut_seq_unequal.py: Trim sequences from a FASTA file in subsequence of the defined size.
* deconseq_run.py: Run DeconSeq automatically and with several threads.
* dimerator.py: Convert a monomer fasta file in a dimer fasta file.
* divnuc_bam.py: Calculate nucleotide diversity per site from BAM files.
* divnuc_plot.py: Calculate nucleotide diversity per window from the output of divnuc_bam.py.
* divsum_ab.py: Used with satminer quantification.
* divsum_count.py: Count the number of nucleotides per elements in a RepeatMasker's divsum file.
* divsum_to_rl.py: Generates satDNA repeat lanscapes using satMiner's criteria.
* dnapipete_createdb.py: Generate a database compatible with RepeatMasker from the dnaPipeTe
* extract_member_reads_rexp.py: Extract reads in a specific cluster of RepeatExplorer.
* extract_no_seq.py: Extract sequecences from a FASTA file absent in a list.
* extract_reads_blat.py: Extract matching reads in a PSL output from BLAT.
* extract_reads_rm.py: Extract matching reads in a OUT output from RepeatMasker.
* extract_regions_bam.py: Extract reads from a BAM only in the indicated regions.
* extract_seq.py: Extract sequences from a FASTA file present in a list conserving the order.
* extract_seq_regions.py: Extract specific regions of sequences from a FASTA file present in a list conserving the order.
* fasta_filter_by_length.py: Filter out sequences from a FASTA file with a size lower than a thereshold.
* fasta_sequence_len.py: Generate a table with the length of each sequence in a FASTA file.
* fastq-combine-pe.py: Extract reads paired reads by ID from two FASTQ files.
* fastq-pe-random.py: Random selection of paired reads from two FASTQ files.
* fastq_edit_ids.py: Edit the ID from FASTQ files to end with the format "@ID/1".
* fastq_edit_ids_sra.py: Edit the ID from FASTQ files to end with the format "@ID/1" from SRA files.
* fastq_paired_combine_id: Extract paired reads looking at its ids.
* find_exclusive_kmers.py: Extract exclusive kmers of a library in comparison with other using Jellyfish.
* gatk_protocol.py: Run GATK in a list of FASTQ files with the same reference.
* get_no_blat.py: Extract sequences from a FASTA file absent in a PSL output of BLAT.
* gff_creator.py: Generate a GFF file for htseq-count from a FASTA file.
* id_rmasker.py: Edit IDs from a FASTA file with a format compatible with RepeatMasker.
* id_rmasker_rexp.py: Edit IDs from a FASTA file of RepeatExplorer contigs compatible with RepeatMasker.
* join_multiple_lists.py: Join the results of two or more lists.
* join_multiple_lists_var.py: Join the results of two or more lists for bam_var_join.py.
* join_rm_list.py: Join two files with RepatMasker nucleotide counts.
* kimura_window.py: Calculate kimura divergence per window using the RepeatMasker's script.
* kmer_to_fasta.py: Generate a FASTA file from a list of kmers.
* mapping_blat_gs.py: Extract matching reads with BLAT and optionally launch Newbler, RepeatMasker or SSAHA2.
* mapping_blat_gs_hard.py: Extract matching reads with hard options of BLAT and optionally launch Newbler, RepeatMasker or SSAHA2.
* mapping_blat_gs_saver.py: Version of mapping_blat_gs.py for big libraries.
* mapping_blat_gs_single_end.py: Version of mapping_blat_gs.py for single-end libraries.
* massive_phylogeny.py: Using an only FASTA file and gene list, it runs RAxML for each gene. 
* massive_phylogenies_figure.py: Generate pdf phylogenies using a list of Newick files. 
* massive_phylogeny_raxml_support.py: Support script for massive_phylogeny.py.
* mitobim_run.py: Run MITObim with several protocols.
* mreps_extract.py: Generate a FASTA file with tandem sequences using a MREPS output.
* reduce_bam.py: Filter out unmapped paired reads from a BAM file.
* remove_ns.py: Remove reads with Ns after a masking.
* replace_patterns: Replace elements in a file.
* repeat_landscape_decimal.py: Generates a repeat landscape table with divergence values adjusted to one decimal (0.1%) from an ALIGN file. 
* repeat_landscape_decimal_050.py: Generates a repeat landscape table with divergence values adjusted to 0.5% from an ALIGN file. 
* repeat_masker_run.py: Run RepeatMasker alignment for small FASTA files.
* repeat_masker_run_big.py: Run RepeatMasker alignment for several big FASTA files.
* rexp_get_cluster.py: Get FASTA file concatenating all the contigs assembled with RepeatExplorer.
* rexp_prepare.py: Generate a FASTA file ready for RepeatExplorer from two FASTQ files.
* rexp_prepare_deconseq: Generate a FASTa file ready for RepeatExplorer from two FASTQ files filtered with DeconSeq.
* rexp_prepare_normaltag: Generate a FASTa file ready for RepeatExplorer from two FASTQ with normal tag (ids ended in /1 or /2).
* rexp_select_contigs: Select most coveraged contigs in a RepeatExplorer's output.
* rm_clas_seq.py: Classify reads aligning or not using a RepeatMasker's output.
* rm_clas_seq_names: Classify reads coinciding with a annotation and aligning or not using a RepeatMasker's output.
* rm_cluster_external.py: Select no homologous reads, group them per annotation of its read pair and clusterize them.
* rm_getseq.py: Extract sequences of the matching regions in a RepeatMasker's output.
* rm_getseq_annot.py: Extract sequences of the matching regions in a RepeatMasker's output and annotate the sequences of the FASTA.
* rm_getseq_split.py: Extract sequences of the matching regions in a RepeatMasker's output annotate and split the sequences in differente FASTAs.
* rm_join_out.py: Concantenate OUT files from several RepeatMasker's run.
* rm_join_tbl.py: Join TBL files from several RepeatMaseker's run.
* rm_homology.py: Find homologies searching with RepeatMasker sequence by sequence.
* run_abyss.py: Run ABySS assembler with a range of kmers.
* sat_cutter.py: Cut satellites in a FASTA alignment to align homologous regions.
* sat_subfam2fam.py: Edit ALIGN file from RepatMasker to calc Kimura divergence by family instead of subfamily.
* satminer_quant.py: satminer quantification protocol.
* search_issr_1nt.py: Count the number of occurrences for each nucleotide before a SRR region to desing ISRR primers.
* search_issr_2nt.py: Count the number of occurrences for each dinucleotide before a SRR region to desing ISRR primers.
* sequence_ref_alt.py: Get sequences with REF and ALT variants after a SNP calling.
* snp_calling_bchr.py: SNP calling for B chromosomes.
* snp_calling_bchr_z10.py: SNP calling for B chromosomes. Alt<10 in ZB.
* snp_calling_dn_ds: Perform a SNP calling to calculate the dn/dS from a BAM file.
* split_illumina.py: Split FASTQ files from Illumina sequencing in several files.
* sra_download.py: Download SRA files using a list of SRA's accesion numbers.
* ssaha2_run.py: Run SSAHA2 mapping in several libraries.
* ssaha2_run_multi.py: Run SSAHA2 mapping for several big libraries and parallized in different threads.
* ssaha2_run_multi_pe_se.py: Run SSAHA2 mapping for several big libraries and parallized in different threads with paired and unpaired reads.
* ssaha2_run_multi_se.py: Run SSAHA2 mapping for several big libraries and parallized in different threads using single-end libraries.
* stampy_protocol.py: Run Stampy mapping.
* subsampler.py: Subsample sequences from FASTA and FASTQ files.
* taxonomy_retrieve.py: Retrieve taxonomy using a Species list.
* trinity_extract_longest.py: Extract the longest contig for each gene in a Trinity assembly.
* trinotate_auto.py: Run Trinotate.
* unshuffle.py: Unshuffle a list of FASTQ files in _1.fastq and _2.fastq.
