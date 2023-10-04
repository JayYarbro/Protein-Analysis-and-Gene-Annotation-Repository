# Install necessary libraries
!pip install pandas
!pip install bioservices

# Import necessary libraries
import pandas as pd
from bioservices import KEGG

# Create a list of gene names
gene_list = ["GeneA", "GeneB", "GeneC", "GeneN"]

# Convert gene names to KEGG IDs
kegg = KEGG()
kegg_ids = [kegg.get_pathway_by_gene(gene, organism="hsa") for gene in gene_list]

# Create a dictionary with gene names and KEGG IDs
gene_dict = {"Gene": gene_list, "KEGG_ID": kegg_ids}

# Convert dictionary to a pandas DataFrame
gene_df = pd.DataFrame(gene_dict)

# Write DataFrame to a TSV file
gene_df.to_csv("gene_list_with_kegg.tsv", sep="\t", index=False)
# Write DataFrame to a TSV file
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
gene_df.to_csv(desktop + "\\gene_list_with_kegg.tsv", sep="\t", index=False)
