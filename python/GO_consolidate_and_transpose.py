import sys
import pandas as pd
#this is run after generate_mapped_id_csv.py in order to demonstrate which GO terms are mapped to each mapped_id (GN).
def consolidate_and_transpose(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Group by 'mapped_id' and concatenate all labels for each group as lists
    consolidated = df.groupby('mapped_id').apply(lambda x: x.drop(columns='mapped_id').values.flatten().tolist())
    
    # Determine the maximum number of labels for any mapped_id to create equal-length rows
    max_labels = max(len(labels) for labels in consolidated)
    
    # Pad each list with empty strings to match the maximum length
    consolidated = consolidated.apply(lambda x: x + [''] * (max_labels - len(x)))
    
    # Convert the consolidated data into a DataFrame, with 'mapped_id' as column headers
    consolidated_df = pd.DataFrame(consolidated.tolist(), index=consolidated.index).T
    
    # Save the transposed DataFrame to a new CSV file
    consolidated_df.to_csv(output_file, index=False)
    print(f"File saved as: {output_file}")

if __name__ == "__main__":
    # Ensure script has the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python consolidate_and_transpose.py input_file output_file")
        sys.exit(1)

    # Assign input and output file names from command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the consolidation and transposition
    consolidate_and_transpose(input_file, output_file)
