import xml.etree.ElementTree as ET
import csv
import sys
import math

# Usage:
# Run this script from the command line by specifying the input XML file and the desired output CSV file.
# Example:
#   python go_XML_parser.py input_file.xml output_file.csv
# This will parse the XML file, extract specified fields, and output them to a CSV file.

def parse_xml_to_csv(input_file, output_file):
    # Read the file in binary mode to handle encoding
    with open(input_file, 'rb') as file:
        content = file.read()
    
    # Try decoding with UTF-16, fall back to UTF-8 if needed
    try:
        content = content.decode('utf-16')
    except UnicodeDecodeError:
        content = content.decode('utf-8')

    # Parse the XML content
    root = ET.fromstring(content)

    # Define CSV header
    headers = ['label', 'neg_log10(FDR)', 'id', 'level', 'number_in_list', 'fold_enrichment', 'fdr'] + [f'mapped_id_{i+1}' for i in range(10)]  # assuming max 10 mapped_ids

    # Prepare data for CSV
    data_rows = []
    for result in root.findall('.//result'):
        term = result.find('term')
        label = term.find('label').text if term.find('label') is not None else ''
        go_id = term.find('id').text if term.find('id') is not None else ''
        level = term.find('level').text if term.find('level') is not None else ''
        
        input_list = result.find('input_list')
        number_in_list = input_list.find('number_in_list').text if input_list.find('number_in_list') is not None else ''
        fold_enrichment = input_list.find('fold_enrichment').text if input_list.find('fold_enrichment') is not None else ''
        fdr = input_list.find('fdr').text if input_list.find('fdr') is not None else ''
        
        # Calculate -log10(FDR)
        log_fdr = -math.log10(float(fdr)) if fdr else ''
        
        mapped_ids = [mapped_id.text for mapped_id in input_list.find('mapped_id_list').findall('mapped_id')]
        
        # Pad mapped_ids to match the header length
        mapped_ids += [''] * (10 - len(mapped_ids))  # ensure we have a consistent column length for mapped_ids
        
        data_rows.append([label, log_fdr, go_id, level, number_in_list, fold_enrichment, fdr] + mapped_ids)

    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_rows)

    print(f"Data has been successfully written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_csv_from_xml.py <input_file.xml> <output_file.csv>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        parse_xml_to_csv(input_file, output_file)
