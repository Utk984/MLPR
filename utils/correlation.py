import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Load the features DataFrame from the Excel file
file = sys.argv[1]
df = pd.read_csv(file)
df = df.fillna(0)
filenames = df["filename"]
df.drop(columns=["filename"], inplace=True)
scaler = StandardScaler()
df = scaler.fit_transform(df)
# Calculate the correlation matrix
df = pd.DataFrame(df)
correlation_matrix = df.corr()
sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
)
plt.title(f"Correlation Matrix - {len(df.columns)} Features")
plt.show()

# Filter out highly correlated features
threshold = 0.8
highly_correlated_features = set()
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > threshold:
            colname_i = correlation_matrix.columns[i]
            highly_correlated_features.add(colname_i)

# Drop highly correlated features from the DataFrame
df_filtered = df.drop(columns=highly_correlated_features)
sns.heatmap(df_filtered.corr(), cmap="coolwarm")
plt.title(f"Correlation Matrix - {len(df_filtered.columns)} Features")
plt.show()

# Save the filtered DataFrame to a new Excel file
df_filtered.insert(0, "filename", filenames)
df_filtered.to_csv("features_filtered_test.csv", index=False)
