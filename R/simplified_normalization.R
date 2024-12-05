# Remove the (#) from the the following 3 lines if you need to install these packages.
#install.packages(readxl)
#install.packages(dplyr)
#install.packages(tibble)

# Load required packages
library(readxl)      # For reading Excel files
library(dplyr)       # For data manipulation
library(tibble)      # For working with row names

# Set working directory (generalizable path, update as needed)
setwd("path/to/your/project/directory")  # Replace with your project's directory path

# Read input data from Excel file. If the data is preformatted, you can just name it df. 
# Ensure the path and file name are updated to the correct location for collaborators
initial_input <- read_excel("input_file.xlsx", 
                            sheet = "trimmed_input", 
                            na = "NA")  # Adjust NA representation as needed

# Create a new dataframe 'df' by:
# - Setting the column "Unique.ID" as row names. Can be any other column but names MUST be unique. 
# - Removing the first 10 columns (as per requirements)
df <- initial_input %>%
  column_to_rownames(var = "Unique.ID") %>%
  select(-(1:10))

# Calculate the global median value of all rows and columns in 'df'
global_median <- median(as.matrix(df), na.rm = TRUE)

# Median normalization
# Compute column-wise medians while ignoring NA values
medians <- apply(df, 2, median, na.rm = TRUE)

# Subtract column medians from each value
df_mednorm <- sweep(df, 2, medians, FUN = "-")

# Standard deviation (SD) normalization
# Compute column-wise standard deviations while ignoring NA values
sds <- apply(df_mednorm, 2, sd, na.rm = TRUE)

# Normalize by dividing each value by the column's SD
df_normalized <- sweep(df_mednorm, 2, sds, FUN = "/")

# Boost normalized values by the global median value
df_boosted <- df_normalized + global_median

# Output the boosted dataframe
# Save or inspect the boosted data as needed for downstream analysis
#write.csv(df_boosted, "boosted_normalized_output.csv")  # Update file name as needed
