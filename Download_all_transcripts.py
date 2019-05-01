from subprocess import run as r
import os

my_env = os.environ.copy()
my_env["PATH"] = "/Users/hughesn/Softwares/sratoolkit.2.9.6-mac64/bin:" + my_env["PATH"]

cmd = "fasterq-dump {0} --split-files --outdir fastq"

print('Started')
for i in range(3345216, 3345279):
    sra = "SRX{0}".format(i)
    print('Getting file: {0}'.format(sra))
    r(cmd.format(sra).split(), env=my_env)

print('All done')
