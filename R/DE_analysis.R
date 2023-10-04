# Load the required R packages
library(readxl) # For reading Excel files
library(dplyr)  # For data manipulation
library(ggplot2) # For creating plots
library(broom)   # For statistical analysis results
library(tibble)  # For data manipulation
library(purrr)   # For data manipulation

# Set the working directory to the input folder on your desktop
setwd("~/Desktop/input_folder")

# Read the data from an Excel file into a data frame
stat_input <- read_excel("input.xlsx", 
    sheet = "input")

# Extract the gene names and convert the remaining data into a matrix
df <- as.matrix(stat_input[,-1])
genes <- (stat_input[,c(1)])

#separate out individual groups from one another. in the code that says (c(a:b)), put the first and last columns including each group. e.g., if columns 1-3 are controls, put c(1:3)
df_ctl <- df[,c(1:3)] %>% data.matrix(.)
de_A <- df[,c(4:6)] %>% data.matrix(.)
de_B <- df[,c(7:9)] %>% data.matrix(.)
de_C <- df[,c(10:12)] %>% data.matrix(.)

# Combine some groups of data
df_transgenic <- cbind(de_FAD_3m, de_FAD_6m, de_FAD_12m, de_J20_6m, de_J20_12m, de_NLF_3m, de_NLF_12m, de_NLGF_3m, de_NLGF_6m, de_NLGF_12m, de_NLGF_18m)

# Combine control data with test data for statistical comparison
df_A <- cbind(de_A, df_ctl)
df_B <- cbind(de_B, df_ctl)
df_C <- cbind(de_c, df_ctl)

# Define groups for the statistical test. In this data, there are 3 ctl and 3 test samples
grp_test <- factor(c(rep("B",3), rep("A",3)))

# Perform statistical tests and adjust for multiple comparisons
mod_A <- mod.t.test(df_A, grp_test, adjust.method = "BH", sort.by = "none")
mod_B <- mod.t.test(df_B, grp_test, adjust.method = "BH", sort.by = "none")
mod_C <- mod.t.test(df_C, grp_test, adjust.method = "BH", sort.by = "none")

# Combine gene information and statistical results
statistical_data <- cbind(genes, mod_A, mod_B, mod_C)

# Write the combined data to a CSV file on your desktop
write_csv(statistical_data, "~/Desktop/stat_data.csv")

#Log2FC cutoffs must be manually calculated. This can be done by porting data into Excel. Calculate the =STDEV(log2) for each sample (raw_SD). Duplicate the sheet (2SD cutoff), cut sample values above/below median+/- 2SD. Recalculate a trimmed SD for each group. This trimmed SD will be the log2 cutoff (+/-2SD)


#Count differentially expressed proteins from output. In this case, the file dep_data is an annotated version of the previously output stat_data.csv, loaded back into R.
A_DEP <- nrow(dep_data$adj.p.value_A <0.05 & (dep_data$'difference in means_A' > (2SD) | dep_data$'difference in means_A' < (-2SD),])
B_DEP <- nrow(dep_data$adj.p.value_B <0.05 & (dep_data$'difference in means_B' > (2SD) | dep_data$'difference in means_B' < (-2SD),])
C_DEP <- nrow(dep_data$adj.p.value_C <0.05 & (dep_data$'difference in means_V' > (2SD) | dep_data$'difference in means_C' < (-2SD),])

# Display the counts of differentially expressed proteins
A_DEP
B_DEP
C_DEP


# Categorize genes as up-regulated, down-regulated, or unchanged
volcano_A <- cbind(genes, mod_A)
volcano_A <- volcano_A %>% 
  mutate(
    Expression = case_when(`difference in means_A` >= (2SD) & adj.p.value <= 0.05 ~ "Up-regulated",
                           `difference in means_A` <= (-2SD) & adj.p.value <= 0.05 ~ "Down-regulated",
                           TRUE ~ "Unchanged")
  )

# Create a volcano plot
p2_A <- ggplot(volcano_A, aes(`difference in means`, -log(adj.p.value,10))) +
  geom_point(aes(color = Expression), size = 3) +
  xlab(expression("log"[2]*"FC(A/ctl)")) + 
  ylab(expression("-log"[10]*"FDR")) +
  #set the boundaries of the x- and y- axis
  #xlim(c(-min,max)) +
  #ylim(c(-min,max)) +
  scale_color_manual(values = c( "dodgerblue3", "gray50", "firebrick3")) +
  guides(colour = guide_legend(override.aes = list(size=3))) +
  theme_minimal() +
  ggtitle("A vs Ctl") +
  geom_vline(xintercept=c(-2SD, 2SD), col="black",linetype="dotdash") +
  geom_hline(yintercept=-log10(0.05), col="black",linetype="dotdash")+
  theme(panel.grid = element_blank(), 
        
        panel.border = element_rect(fill= "transparent"), legend.text=element_text(size=22), legend.title=element_text(size=21),
        axis.title=element_text(size=22,face="bold"),axis.text.x = element_text(face="bold", color="black", 
                                                                                size=20, angle=0),
        axis.text.y = element_text(face="bold", color="black", 
                                   size=20, angle=0),legend.position = "none",
        plot.title = element_text(color="black", size=22, face="bold",hjust =0.5))

# Display the volcano plot
p2_A
