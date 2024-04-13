import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load data from CSV
data = pd.read_csv("pca.csv")

# Extract file names
file_names = data.iloc[:, 0]

# Extract feature columns for clustering
features = data.iloc[:, 1:]

# Initialize a list to store silhouette scores
silhouette_scores = []

# Let's try K values from 2 to 10
for k in range(2, 20):
    # Create KMeans model
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    # Fit the model to the scaled features
    kmeans.fit(features)
    # Get the cluster labels
    labels = kmeans.labels_
    # Compute silhouette score
    silhouette_avg = silhouette_score(features, labels)
    silhouette_scores.append(silhouette_avg)
    print(f"For K={k}, silhouette score is {silhouette_avg}")

# Find the best K value based on silhouette score
print("\nSilhouette scores:", silhouette_scores)
best_k = np.argmax(silhouette_scores) + 2
print(f"\nBest K value based on silhouette score: {best_k}")

# Finally, train KMeans with the best K value
best_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
best_kmeans.fit(features)

# Assign cluster labels to the original data
df = pd.DataFrame(file_names, columns=["File"])
df["Cluster"] = best_kmeans.labels_

# Save results to a new CSV file
df.to_csv("clustered_data.csv", index=False)
