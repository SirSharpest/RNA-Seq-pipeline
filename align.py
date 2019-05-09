from glob import glob
from subprocess import run as r
from os import cpu_count
from os.path import exists as exists
from os import makedirs as mkdir
import argparse
from os.path import basename


def run_alignment(reference, inFile, outDir, outFile, inFileR=None):
    if inFileR is not None:
        cmd = "hisat2 -x {0} -1 {1} -2 {2} -p {3} | samtools view -bh - | samtools sort - > {4}/{5}.bam"
        sh = cmd.format(reference, inFile, inFileR,
                        cpu_count(), outDir, outFile)
    else:
        cmd = "hisat2 -x {0} -U {1} -p {2} | samtools view -bh - | samtools sort - > {3}/{4}.bam"
        sh = cmd.format(reference, inFile, cpu_count(), outDir, outFile)
    print(sh)
    r(sh, shell=True)
    run_index("{0}/{1}.bam".format(outDir, outFile))


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
    ap.add_argument("-F", "--forward", required=False,
                    help="FASTQ Forward files ID")
    ap.add_argument("-R", "--reverse", required=False,
                    help="FASTQ files reverse ID")
    ap.add_argument("-r", "--reference", required=True,
                    help="Reference index file(s)")
    ap.add_argument("-o", "--output", required=True,
                    help="Output Folder")
    args = vars(ap.parse_args())
    return args


def main():
    args = get_args()

    if 'forward' in args:
        f_files = glob(
            "{0}/*{1}.fq.gz".format(args['fastq'], args['forward']))
        r_files = glob(
            "{0}/*{1}.fq.gz".format(args['fastq'], args['reverse']))
        if len(f_files) == 0:
            f_files = glob(
                "{0}/*{1}.fastq".format(args['fastq'], args['forward']))
            r_files = glob(
                "{0}/*{1}.fastq".format(args['fastq'], args['reverse']))
        f_files.sort()
        r_files.sort()

        if not exists(args["output"]):
            mkdir(args["output"])

            for f, rv in zip(f_files, r_files):
                fname = basename(f).split('.')[0]
                run_alignment(args['reference'], f,
                              args['output'], fname, inFileR=rv)
    else:
        fastq = glob("{0}/*.fastq")
        if len(fastq) == 0:
            fastq = glob("{0}/*.fq.gz")
        for f in fastq:
            fname = basename(f).split('.')[0]
            run_alignment(args['reference'], f, args['output'], fname)


if __name__ == '__main__':
    main()
