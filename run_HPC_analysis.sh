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

FASTQ="../arabidopsis_thaliana/seedling_data/raw/"
FASTQ_R="../arabidopsis_thaliana/seedling_data/raw/"
FASTQ_O="../arabidopsis_thaliana/seedling_data/fastq/"
FASTQ_O_R="../arabidopsis_thaliana/seedling_data/fastq/"
FORWARD_I = "_1"
REVERSE_I = "_2"
REPORTS="../arabidopsis_thaliana/seedling_data/reports"
INDEX="../arabidopsis_thaliana/Reference/hisat2_index/arabidopsis.hisat2"
BAM="../arabidopsis_thaliana/seedling_data/bam"
GTF="../arabidopsis_thaliana/Reference/Arabidopsis_thaliana.TAIR10.43.gtf"
HTSEQ_COUNT="../arabidopsis_thaliana/seedling_data/htseq-count"
ADAPTORS="../arabidopsis_thaliana/Adaptors/novogene.fa"

#Perform adaptor removal
python3 ./remove_adaptors.py -f $FASTQ -r $FASTQ_R -F -R -a -u -I

# Perform fastqc analysis
# -> reports and multiqc report
#python3 ./qc.py -f $FASTQ -o $REPORTS

# align the fastq to annotation
# fastq -> bam
#python3 ./align.py -f $FASTQ -r $INDEX -o $BAM

# bam -> counts
#python3 ./count_genes.py -b $BAM -g $GTF -o $HTSEQ_COUNT
