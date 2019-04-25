zea_ref=./Reference/hisat2_index/Zea_mays.hisat2
for p in ./fastq/*.fastq; do
    hisat2 -x zea_ref -U $p | samtools view -bh - | samtools sort - > "./bam/$p.bam"
    samtools index "./bam/$p"
    echo "./bam/$p  is done!"
done
