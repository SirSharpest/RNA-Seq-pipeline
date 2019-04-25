while read p; do
    hisat2 -x ./Reference/GCF_000005005.hisat2 -U $p | samtools view -bh - | samtools sort - > "./bam/$p.bam"
    samtools index "./bam/$p"
    echo "./bam/$p  is done!"
done <list_of_fixed_files.txt
