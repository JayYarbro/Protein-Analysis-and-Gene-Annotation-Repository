# Adapted from code written by Aijun Zhang.

# Load required packages
library(dplyr)
library(plotly)
library(DT)

# Assume `variables$result` is your data frame with differential expression results.
# You can load your data frame directly here for testing.
# data <- read.csv("your_data_file.csv")  # Uncomment to load your own data
data <- variables$result  # Replace this line with your own data if needed

# Define bin size for moving SD calculation
binsize <- 1000  # Modify as needed for your analysis

# Data processing
# Keep only intensity value columns by removing p-value and FDR columns
data <- data %>% dplyr::select(-contains(c("p-value", "FDR")))

# Calculate mean intensity for ordering
data$mean_intensity <- rowMeans(data %>% select(-Log2Fold), na.rm = TRUE)
data <- data[order(data$mean_intensity, decreasing = FALSE), ]

# Calculate moving standard deviation
end <- nrow(data) - binsize + 1
moving_sd <- sapply(1:end, function(i) {
  last <- i + binsize - 1
  sd(data$Log2Fold[i:last], na.rm = TRUE)
})

# For remaining entries where bin size cannot be covered, use the last moving SD
moving_sd_remain <- rep(moving_sd[length(moving_sd)], nrow(data) - end)
moving_sd <- c(moving_sd, moving_sd_remain)

# Store moving SDs in data frame
data$movingSD <- moving_sd

# Calculate z-scores for Log2Fold change
data$logFC_z_score <- data$Log2Fold / data$movingSD

# Add back p-value and FDR columns from the original dataset (dfx)
data <- cbind(data, dfx[, c("p-value", "FDR")])

# Plot the moving SD vs mean intensity using Plotly
plot <- plot_ly(
  data = data,
  x = ~mean_intensity,
  y = ~movingSD,
  type = "scatter",
  mode = "markers"
) %>%
  layout(
    title = paste("Moving SD of proteomic data, bin size =", binsize),
    xaxis = list(title = "log2 protein intensity"),
    yaxis = list(title = "Moving SD", range = c(0, 1))
  ) %>%
  plotly::config(
    toImageButtonOptions = list(
      format = "svg",
      filename = "Moving_SD_Plot"
    )
  )

# Display plot
print(plot)
