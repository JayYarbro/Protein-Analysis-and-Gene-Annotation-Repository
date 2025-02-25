# Load necessary library
library(dplyr)
library(readr)

setwd("your_directory")

# Prepare data 
data(mtcars)
cars <- mtcars[, c(1:4, 6:7, 9:11)]  # Select desired columns

# Compute hierarchical clustering using pipes
hc <- cars %>%
  dist() %>%
  hclust()

plot(hc)
# Convert hclust object to a dendrogram for recursive processing
dend <- as.dendrogram(hc)

assign_cluster_labels <- function(dend, current_label = "") {
  # helper function to count the number of leaves in a dendrogram node
  count_leaves <- function(d) {
    if (is.leaf(d)) return(1)
    else return(sum(sapply(d, count_leaves)))
  }
  
  # If this node is a leaf, return its sample name with the current label.
  if (is.leaf(dend)) {
    return(data.frame(Sample = attr(dend, "label"), 
                      Cluster = current_label, 
                      stringsAsFactors = FALSE))
  } else {
    # Get the two children of this node
    left_child <- dend[[1]]
    right_child <- dend[[2]]
    left_count  <- count_leaves(left_child)
    right_count <- count_leaves(right_child)
    
    # If both children have at least 2 samples, we consider this node to be splittable.
    if (left_count >= 2 && right_count >= 2) {
      # For the top-level (current_label == ""), use "1" and "2"
      new_label_left  <- if (current_label == "") "1" else paste0(current_label, ".1")
      new_label_right <- if (current_label == "") "2" else paste0(current_label, ".2")
      
      # Recursively assign labels to both branches.
      left_df  <- assign_cluster_labels(left_child, new_label_left)
      right_df <- assign_cluster_labels(right_child, new_label_right)
      
      return(rbind(left_df, right_df))
    } else {
      # Otherwise, we stop splitting here.
      # (For example, if one branch is a single sample, we take the whole node as one cluster.)
      final_label <- if (current_label == "") "1" else current_label
      # Get all sample names (leaf labels) from this node.
      leaf_labels <- labels(dend)
      return(data.frame(Sample = leaf_labels, 
                        Cluster = final_label, 
                        stringsAsFactors = FALSE))
    }
  }
}


cluster_df <- assign_cluster_labels(dend)
print(cluster_df)
write_csv(cluster_df, "cluster_df.csv")
