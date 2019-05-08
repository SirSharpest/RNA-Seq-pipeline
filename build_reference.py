from subprocess import run as r
from os import cpu_count
cores = cpu_count()
# Index reference genome
hisat_dir = "mkdir -p ./Reference/hisat2_index"
r(hisat_dir.split())

with open('./Reference/hisat2_index/splice_sites.txt', 'w') as f:
    splice_sites = "hisat2_extract_splice_sites.py -v ./Reference/Arabidopsis_thaliana.TAIR10.43.gtf"
    r(splice_sites.split(), stdout=f)


with open('./Reference/hisat2_index/exons.txt', 'w') as f:
    exons = "hisat2_extract_exons.py -v ./Reference/Arabidopsis_thaliana.TAIR10.43.gtf "
    r(exons.split(), stdout=f)

hisat_build = "hisat2-build ./Reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa --ss ./Reference/hisat2_index/splice_sites.txt --exon ./Reference/hisat2_index/exons.txt ./Reference/hisat2_index/arabidopsis.hisat2 -p {0}".format(
    cores)
r(hisat_build.split())
