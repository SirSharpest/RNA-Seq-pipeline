from os import cpu_count
from subprocess import run as run
from os.path import basename
from glob import glob
import argparse


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
    ap.add_argument("-I", "--identiferR", required=True,
                    help="reverse identifier")

    args = vars(ap.parse_args())
    return args


def main():
    args = get_args()
    threads = cpu_count()
    f_files = glob("{0}/{1}*".format(args['forward'], args['identifier']))
    r_files = glob("{0}/{1}*".format(args['reverse'], args['identifierR']))

    adaptors = args["adaptors"]
    for f, r in zip(f_files, r_files):
        out_f = "{0}/trimmed_{1}".format(args['FORWARDOUT'], basename(f))
        out_r = "{0}/trimmed_{1}".format(args['REVERSEOUT'], basename(r))
        cmd = "srun java -jar '/nbi/software/testing/trimmomatic/0.33/x86_64/bin/trimmomatic-0.33.jar' PE -threads {4} \
             -phred33 {0} {1} {2} {3} ILLUMINACLIP:{4}:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36".format(f, r,
                                                                                                                         out_f, out_r,
                                                                                                                         adaptors, threads)
        run(cmd, shell=True)


if __name__ == '__main__':
    main()
