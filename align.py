from glob import glob
from subprocess import run as r
from os import cpu_count
from os.path import exists as exists
from os import makedirs as mkdir
import argparse
from os import basename


def run_alignment(reference, inFile, outDir, outFile):
    cmd = "hisat2 -x {0} -U {1} -p {2}| samtools view -bh - | samtools sort - > {3}/{4}.bam"
    sh = cmd.format(reference, inFile, cpu_count(), outDir, outFile)
    print(sh)
    r(sh, shell=True)
    run_index(inFile)


def index_all(startDir):
    for f in glob("{0}/*.bam".format(startDir)):
        run_index(f)


def run_index(inFile):
    cmd = "samtools index {0}".format(inFile)
    r(cmd, shell=True)
    print('Done indexing: {0}'.format(inFile))


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fastq", required=True,
                    help="FASTQ files location")
    ap.add_argument("-r", "--reference", required=True,
                    help="Reference index file(s)")
    ap.add_argument("-o", "--output", required=True,
                    help="Output Folder")
    args = vars(ap.parse_args())
    return args


def main():
    args = get_args
    fastq = glob('{0}*.fastq').format(args['fastq'])
    total = len(fastq)
    if not exists(args["output"]):
        mkdir(args["output"])
    for idx, f in enumerate(fastq):
        print('{0} of {1}'.format(idx, total))
        fname = basename(f).split('.')[0]
        run_alignment(args['reference'], f, args['output'], fname)


if __name__ == '__main__':
    main()
