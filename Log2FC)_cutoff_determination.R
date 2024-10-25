# User-defined variables
n <- 2  # Default value for nTSD, can be changed by the user
outlier_nSD <- 2  # Default for outlier threshold, can be altered by the user

# Store Log2Fold column
log2_fold_values <- data$Log2Fold

# Calculate initial statistics
log2_fold_sd <- sd(log2_fold_values, na.rm = TRUE)
log2_fold_median <- median(log2_fold_values, na.rm = TRUE)

# Determine outlier threshold range based on median ± outlier_nSD * standard deviation
lower_bound <- log2_fold_median - (outlier_nSD * log2_fold_sd)
upper_bound <- log2_fold_median + (outlier_nSD * log2_fold_sd)

# Create trimmed list excluding outliers
trimmed_log2_fold <- log2_fold_values[log2_fold_values >= lower_bound & log2_fold_values <= upper_bound]

# Calculate trimmed standard deviation (tSD)
trimmed_sd <- sd(trimmed_log2_fold, na.rm = TRUE)

# Calculate the final cutoff using nTSD
log2_fold_cutoff <- n * trimmed_sd

# Return result
cat("Your log2-fold cutoff is |", log2_fold_cutoff, "|")
