#!/bin/bash
#SBATCH --job-name="RNA-seq analysis"
#SBATCH --output=RNA-seq-analysis.txt
#SBATCH --partition=jic-medium
#SBATCH --cpus-per-task=30
#SBATCH --mem 200G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nathan.hughes@jic.ac.uk

source python-3.5.1
source /hpc-home/hughesn/Transcriptomics/bin/activate
source hisat-2.1.0
source samtools-1.5
source htseq-0.9.1
source fastqc-0.11.3

FASTQ="../arabidopsis_thaliana/SRA_Data/fastq/"
REPORTS="../arabidopsis_thaliana/SRA_Data/reports"
INDEX="../arabidopsis_thaliana/Reference/hisat2_index/arabidopsis.hisat2"
BAM="../arabidopsis_thaliana/SRA_Data/bam"
GTF="../arabidopsis_thaliana/Reference/Arabidopsis_thaliana.TAIR10.43.gtf"
HTSEQ_COUNT="../arabidopsis_thaliana/SRA_Data/htseq-count"
ADAPTORS="../arabidopsis_thaliana/Adaptors/novogene.fa"

#Perform adaptor removal
# srun java -jar "/nbi/software/testing/trimmomatic/0.33/x86_64/bin/trimmomatic-0.33.jar" PE \
#      -phred33 input_forward.fq.gz input_reverse.fq.gz \
#      output_forward_paired.fq.gz output_forward_unpaired.fq.gz\
#      output_reverse_paired.fq.gz output_reverse_unpaired.fq.gz \
#      ILLUMINACLIP:${ADAPTORS}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

# Perform fastqc analysis
# -> reports and multiqc report
python3 ./qc.py -f $FASTQ -o $REPORTS

# align the fastq to annotation
# fastq -> bam
python3 ./align.py -f $FASTQ -r $INDEX -o $BAM

# bam -> counts
python3 ./count_genes.py -b $BAM -g $GTF -o $HTSEQ_COUNT
