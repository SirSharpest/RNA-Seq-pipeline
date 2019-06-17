from os import cpu_count
from subprocess import run as run
from os.path import basename
from glob import glob
import argparse
from os.path import exists as exists
from os import makedirs as mkdir


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--forward", required=True,
                    help="Forward read folder")
    ap.add_argument("-r", "--reverse", required=True,
                    help="Reverse read folder")
    ap.add_argument("-F", "--FORWARDOUT", required=True,
                    help="Forward out folder")
    ap.add_argument("-R", "--REVERSEOUT", required=True,
                    help="Reverse out folder")
    ap.add_argument("-a", "--adaptors", required=True,
                    help="Adaptors to use")
    ap.add_argument("-i", "--identifier", required=True,
                    help="forward identifier")
    ap.add_argument("-I", "--identifierR", required=True,
                    help="reverse identifier")
    ap.add_argument("-T", "--Trimmomatic", required=True,
                    help="Trimmomatic jar software link")

    args = vars(ap.parse_args())
    return args


def main():
    args = get_args()
    threads = int(cpu_count()) - 1
    f_files = glob(
        "{0}/*{1}.fq.gz".format(args['forward'], args['identifier']))
    r_files = glob(
        "{0}/*{1}.fq.gz".format(args['reverse'], args['identifierR']))

    f_files.sort()
    r_files.sort()
    adaptors = args["adaptors"]
    if not exists(args["FORWARDOUT"]):
        mkdir(args["FORWARDOUT"])
    if not exists(args["REVERSEOUT"]):
        mkdir(args["REVERSEOUT"])

    trimmomatic = args['Trimmomatic']
    for f, r in zip(f_files, r_files):
        out_f = "{0}/trimmed_{1}".format(args['FORWARDOUT'], basename(f))
        out_r = "{0}/trimmed_{1}".format(args['REVERSEOUT'], basename(r))
        cmd = "java -jar '{6}' PE -threads {5} \
             -phred33 {0} {1} {2} unpaired_1.fa.gz  {3} unpaired_2.fa.gz ILLUMINACLIP:{4}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36".format(f, r,
                                                                                                                                                            out_f, out_r,
                                                                                                                                                            adaptors, threads, trimmomatic)
        run(cmd, shell=True)


if __name__ == '__main__':
    main()
