#!/bin/bash
#SBATCH --job-name="RNA-seq Alignment"
#SBATCH --output=RNA-seq-analysis.txt
#SBATCH --partition=jic-medium
#SBATCH --cpus-per-task=30
#SBATCH --mem 200G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nathan.hughes@jic.ac.uk

source python-3.5.1
source /hpc-home/hughesn/Transcriptomics/bin/activate
source hisat2-2.1.0
source samtools-1.5
source htseq-0.9.1
source fastqc-0.11.3

FASTQ="../arabidopsis_thaliana/seedling_data/raw/raw_data/"
FASTQ_R="../arabidopsis_thaliana/seedling_data/raw/raw_data/"
FASTQ_O="../arabidopsis_thaliana/seedling_data/fastq/"
FASTQ_O_R="../arabidopsis_thaliana/seedling_data/fastq/"
FORWARD_I="_1"
REVERSE_I="_2"
REPORTS="../arabidopsis_thaliana/seedling_data/reports"
TRIMMED_REPORTS="../arabidopsis_thaliana/seedling_data/trimmed_reports"
INDEX="../arabidopsis_thaliana/Reference/hisat2_index/arabidopsis.hisat2"
BAM="../arabidopsis_thaliana/seedling_data/bam"
GTF="../arabidopsis_thaliana/Reference/Arabidopsis_thaliana.TAIR10.43.gtf"
HTSEQ_COUNT="../arabidopsis_thaliana/seedling_data/htseq-count"
ADAPTORS="universal.fa"
TRIMMOMATIC_NBI="/nbi/software/testing/trimmomatic/0.33/x86_64/bin/trimmomatic-0.33.jar"

echo "Running pre qc"
python3 ./qc.py -f $FASTQ -o $REPORTS

#Perform adaptor removal
echo "Adaptor trimming"
python3 ./remove_adaptors.py -f ${FASTQ} -r ${FASTQ_R} -F ${FASTQ_O} -R ${FASTQ_O_R} -a ${ADAPTORS} -i ${FORWARD_I} -I ${REVERSE_I} -T ${TRIMMOMATIC_NBI}

# Perform fastqc analysis
# -> reports and multiqc report post trimming
echo "Running post qc"
python3 ./qc.py -f ${FASTQ} -o ${TRIMMED_REPORTS}

# align the fastq to annotation
# fastq -> bam
echo "Performing align"
python3 ./align.py -f ${FASTQ} -r ${INDEX} -o ${BAM} -F ${FORWARD_I} -R ${REVERSE_I}

# bam -> counts
python3 ./count_genes.py -b ${BAM} -g ${GTF} -o ${HTSEQ_COUNT}
