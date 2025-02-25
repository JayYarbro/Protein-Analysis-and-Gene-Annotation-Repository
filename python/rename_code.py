import csv
import os

# Read the rename mapping from Rename.csv
rename_dict = {}
with open('Rename.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rename_dict[row['Name1']] = row['name2']

def process_file(input_file, output_file):
    with open(input_file, newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        for row in reader:
            # Skip empty rows
            if not row:
                continue
            # If the header row's first cell does not end with ".d", leave it unchanged.
            if row[0].endswith('.d'):
                # Extract the basename (the filename at the end of the path)
                base = os.path.basename(row[0])
                # If the basename is in mapping, replace it.
                if base in rename_dict:
                    new_base = rename_dict[base]
                    # Rebuild the path with the new filename
                    row[0] = os.path.join(os.path.dirname(row[0]), new_base)
            writer.writerow(row)

# Process both report files
process_file('report.tsv', 'report_rename.tsv')
