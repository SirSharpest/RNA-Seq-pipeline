from os.path import exists as exists
from os import makedirs as mkdir
from glob import glob as glob
from subprocess import run as r
from shutil import move as mv

# Make references dir
if not exists('Reference'):
    mkdir('Reference')


r(['wget', 'ftp://ftp.ensemblgenomes.org/pub/plants/release-43/fasta/arabidopsis_thaliana/dna/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz'])
r(['wget', 'ftp://ftp.ensemblgenomes.org/pub/plants/release-43/gtf/arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.43.gtf.gz'])
for f in glob('*.gz'):
    r(['gunzip', f])

for f in ['Arabidopsis_thaliana.TAIR10.dna.toplevel.fa', 'Arabidopsis_thaliana.TAIR10.43.gtf']:
    mv(f, 'Reference/{0}'.format(f))
