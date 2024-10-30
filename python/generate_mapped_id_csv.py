import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict

# Usage:
# Run this script from the command line by specifying the input XML file and the desired output CSV file.
# Example:
#   python generate_mapped_id_csv.py input_file.xml output_file.csv
# This will parse the XML file, extract specified fields, and output them to a CSV file.

def parse_xml_to_mapped_id_csv(input_file, output_file):
    # Read the file in binary mode to handle encoding issues
    with open(input_file, 'rb') as file:
        content = file.read()

    # Try decoding with UTF-8, fall back to UTF-16 if needed
    try:
        content = content.decode('utf-8')
    except UnicodeDecodeError:
        content = content.decode('utf-16')

    # Parse the XML content from the string
    root = ET.fromstring(content)

    # Dictionary to store each mapped_id and its associated labels
    mapped_id_dict = defaultdict(set)

    # Iterate over results and collect labels per mapped_id
    for result in root.findall('.//result'):
        label = result.find('term/label').text if result.find('term/label') is not None else ''
        mapped_ids = result.find('input_list/mapped_id_list')

        if mapped_ids is not None:
            for mapped_id in mapped_ids.findall('mapped_id'):
                mapped_id_dict[mapped_id.text].add(label)

    # Define CSV header
    max_labels = max(len(labels) for labels in mapped_id_dict.values())
    headers = ['mapped_id'] + [f'label_{i+1}' for i in range(max_labels)]

    # Prepare data for CSV
    data_rows = []
    for mapped_id, labels in mapped_id_dict.items():
        row = [mapped_id] + list(labels) + [''] * (max_labels - len(labels))  # Ensure consistent column count
        data_rows.append(row)

    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_rows)

    print(f"Data has been successfully written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_mapped_id_csv.py <input_file.xml> <output_file.csv>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        parse_xml_to_mapped_id_csv(input_file, output_file)
