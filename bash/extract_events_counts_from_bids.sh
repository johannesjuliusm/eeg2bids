#!/bin/bash

# Define directories
SEARCH_DIR="/Users/jjm/Desktop/rawdata"
DEST_DIR="/Users/jjm/Desktop/rawdata/derivatives/qc"

# Create destination directory if it does not exist
mkdir -p "$DEST_DIR"

# Define BIDS combinations
COMBINATIONS=(
    "ses-m1_task-sl"
    "ses-m12_task-sl"
    "ses-m12_task-mem_acq-learn"
    "ses-m12_task-mem_acq-recall"
)

# Loop over combinations
for combo in "${COMBINATIONS[@]}"; do
    OUTPUT_CSV="$DEST_DIR/${combo}_events_counts.csv"

    # Remove old output file if it exists
    [ -f "$OUTPUT_CSV" ] && rm "$OUTPUT_CSV"

    # Write header
    echo "filename,n_events" > "$OUTPUT_CSV"

    # Find matching events.tsv files and count rows
    find "$SEARCH_DIR" -type f -name "*${combo}*_events.tsv" | sort | while read -r tsv_file; do
        row_count=$(tail -n +2 "$tsv_file" | wc -l | tr -d ' ')
        filename=$(basename "$tsv_file")
        echo "$filename,$row_count" >> "$OUTPUT_CSV"
    done

    echo "Saved row counts for $combo to $OUTPUT_CSV"
done
