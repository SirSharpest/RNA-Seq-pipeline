while read p; do
    ./fix_transfer_errors.pl $p > "$p-fixed.fastq"
    echo "$p - fixed"
done <list_of_files.txt
