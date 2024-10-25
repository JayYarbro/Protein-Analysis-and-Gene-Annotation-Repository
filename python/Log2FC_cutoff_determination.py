import numpy as np
import pandas as pd

# User-defined variables
n = 2  # Default value for nTSD, can be changed by the user
outlier_nSD = 2  # Default for outlier threshold, can be altered by the user

# Assuming `data` is a pandas DataFrame with a 'Log2Fold' column
log2_fold_values = data['Log2Fold']

# Calculate initial statistics
log2_fold_sd = log2_fold_values.std(skipna=True)
log2_fold_median = log2_fold_values.median(skipna=True)

# Determine outlier threshold range based on median ± outlier_nSD * standard deviation
lower_bound = log2_fold_median - (outlier_nSD * log2_fold_sd)
upper_bound = log2_fold_median + (outlier_nSD * log2_fold_sd)

# Create trimmed list excluding outliers
trimmed_log2_fold = log2_fold_values[(log2_fold_values >= lower_bound) & (log2_fold_values <= upper_bound)]

# Calculate trimmed standard deviation (tSD)
trimmed_sd = trimmed_log2_fold.std(skipna=True)

# Calculate the final cutoff using nTSD
log2_fold_cutoff = n * trimmed_sd

# Print result
print(f"Your log2-fold cutoff is | {log2_fold_cutoff} |")
