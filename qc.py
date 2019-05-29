from os import cpu_count
from subprocess import run as r
import argparse
from os.path import exists as exists
from os import makedirs as mkdir


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fastq", required=True,
                    help="FASTQ files location")
    ap.add_argument("-o", "--output", required=True,
                    help="Output Folder")

    args = vars(ap.parse_args())
    return args


def main():
    args = get_args()
    # Make references dir
    if not exists(args["output"]):
        mkdir(args["output"])

    runFastQC = "fastqc -o {0} {1}/*.fq.gz -t {2}".format(
        args['output'], args['fastq'], cpu_count())
    runMultiQC = "multiqc {0} -n {0}/report.html".format(args['output'])

    r(runFastQC, shell=True)
    r(runMultiQC, shell=True)
    print('Done')


if __name__ == '__main__':
    main()
