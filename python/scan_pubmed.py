#pip install biopython

import pandas as pd
from Bio import Entrez

# Function to search PubMed and return the number of hits
def search_pubmed(query):
    Entrez.email = "your.email@example.com"  # Replace with your email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
    record = Entrez.read(handle)
    return int(record["Count"])

# Load the CSV file
input_file = "input.csv"  # Replace with your input CSV file path
output_file = "output.csv"  # Replace with your desired output CSV file path

df = pd.read_csv(input_file)

# Create a new column for storing the number of hits
df['Hits'] = df['Query'].apply(search_pubmed)

# Save the updated dataframe to a new CSV file
df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")
