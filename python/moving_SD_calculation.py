# Import required packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Assume `variables['result']` is your DataFrame with differential expression results.
# You can load your DataFrame directly here for testing.
# data = pd.read_csv("your_data_file.csv")  # Uncomment to load your own data
data = variables['result']  # Replace this line with your own data if needed

# Define bin size for moving SD calculation
binsize = 1000  # Modify as needed for your analysis

# Data processing
# Keep only intensity value columns by removing p-value and FDR columns
data = data.loc[:, ~data.columns.str.contains("p-value|FDR")]

# Calculate mean intensity for ordering
data['mean_intensity'] = data.drop(columns=['Log2Fold']).mean(axis=1, skipna=True)
data = data.sort_values('mean_intensity', ascending=True)

# Calculate moving standard deviation
end = len(data) - binsize + 1
moving_sd = [data['Log2Fold'].iloc[i:i + binsize].std() for i in range(end)]

# For remaining entries where bin size cannot be covered, use the last moving SD
moving_sd_remain = [moving_sd[-1]] * (len(data) - end)
moving_sd.extend(moving_sd_remain)

# Store moving SDs in data frame
data['movingSD'] = moving_sd

# Calculate z-scores for Log2Fold change
data['logFC_z_score'] = data['Log2Fold'] / data['movingSD']

# Add back p-value and FDR columns from the original dataset (dfx)
data = pd.concat([data, dfx[['p-value', 'FDR']]], axis=1)

# Plot the moving SD vs mean intensity using Plotly
fig = go.Figure(
    data=go.Scatter(
        x=data['mean_intensity'],
        y=data['movingSD'],
        mode='markers',
    )
)
fig.update_layout(
    title=f"Moving SD of proteomic data, bin size = {binsize}",
    xaxis_title="log2 protein intensity",
    yaxis_title="Moving SD",
    yaxis=dict(range=[0, 1])
)
fig.update_layout(
    plot_bgcolor='white',
    toImageButtonOptions=dict(
        format="svg",
        filename="Moving_SD_Plot"
    )
)

# Display plot
fig.show()
