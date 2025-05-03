awk '{
    # Check if the line has only 3 fields: date, invoice code, and invoice amount
    if (NF == 3) {
        # Print date and invoice amount
        print $1, $3
    }
}' I.file | sort -t' ' -k1,1 -k2,2n

