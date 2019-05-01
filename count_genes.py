from os import cpu_count
from os.path import basename
from multiprocessing import Pool
from glob import glob
from subprocess import run as r
from os.path import exists as exists
from os import makedirs as mkdir
import argparse


def get_args():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-b", "--bam", required=True, help="BAM files location")
    ap.add_argument("-g", "--gtf", required=True, help="GTF annotation file")
    ap.add_argument("-o", "--output", required=True, help="Output Folder")
    args = vars(ap.parse_args())
    return args


def main():
    args = get_args()
    count_cmd = "htseq-count -f bam -s yes -i gene_id {0} {1} > {2}/{3}_htseq-count.txt"
    bam = glob('{0}/*.bam'.format(args["bam"]))

    def count_genes(bamFile):
        outFile = basename(bamFile).split('.')[0]
        r(count_cmd.format(bamFile, args["gtf"],
                           args["output"], outFile), shell=True)
        return bamFile

    # Make references dir
    if not exists(args["output"]):
        mkdir(args["output"])

    with Pool(cpu_count()) as p:
        p.map(count_genes, bam)


if __name__ == '__main__':
    main()
