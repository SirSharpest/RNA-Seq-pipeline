from os import rename
from glob import glob as g
from get_sra_description import get_name

bams = g('./bam/*.bam')

for b in bams:
    try:
        fn = b.rsplit('/')[-1].rsplit('.bam')[0]
        nn = ''.join(get_name(fn).rsplit(';')[
                     :-1]).replace(' ', '_').replace('\\xa0 ', '')
        print(fn, '-->', nn)
        rename(b, './bam/{0}.bam'.format(nn))
    except Exception:
        print('already renamed, or filename is wrong')
        continue
