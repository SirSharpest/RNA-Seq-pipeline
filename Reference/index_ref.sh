#!/bin/bash
mkdir hisat2_index
hisat2_extract_splice_sites.py -v ./Zea_mays.AGPv3.22.gtf  > hisat2_index/splice_sites.txt
hisat2_extract_exons.py -v ./Zea_mays.AGPv3.22.gtf  > hisat2_index/exons.txt
hisat2-build ./Zea_mays.AGPv3.22.dna_sm.genome.fa --ss ./hisat2_index/splice_sites.txt --exon ./hisat2_index/exons.txt ./hisat2_index/Zea_mays.hisat2 -p 4
