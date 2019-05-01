#!/bin/bash
#SBATCH --job-name="RNA-seq analysis"
#SBATCH --output=RNA-seq-analysis.txt
#SBATCH --partition=jic-medium
#SBATCH --cpus-per-task=30
#SBATCH --mem 200G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nathan.hughes@jic.ac.uk

source python-3.5.1
source ~/modelling/bin/activate
source hisat-2.0.4
source samtools-1.5
source htseq-0.9.1
source fastqc-0.11.3

FASTQ="../fastq"
REPORTS="../reports"
INDEX="../Reference/hisat2_index/hisat2_index"
BAM="../bam"
GTF="../Reference/arabidopsis.gtf"
HTSEQ_COUNT="../HTSEQ_COUNT"

#Perform adaptor removal

# Perform fastqc analysis
# -> reports and multiqc report
srun python3 ./qc.py -f $FASTQ -o $REPORTS

# align the fastq to annotation
# fastq -> bam
srun python3 ./align.py -f $FASTQ -r $INDEX -o $BAM

# bam -> counts
srun python3 ./count_genes.py -b $BAM -g $GTF -o $HTSEQ_COUNT
