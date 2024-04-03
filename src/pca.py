import sys

import pandas as pd
from sklearn.decomposition import PCA


def pca(X, min_variance_ratio=0.95):
    for i in range(0, len(X[0])):
        pca = PCA(n_components=i)
        pca.fit(X)
        if sum(pca.explained_variance_ratio_) > min_variance_ratio:
            num_components = i
            break
    return PCA(n_components=num_components).fit_transform(X)


def reduced(file, output_file):
    data = pd.read_csv(file)
    data.drop(data.columns[0], axis=1, inplace=True)
    X = data.iloc[:, :-1].values
    X_transformed = pca(X)

    # Convert transformed data to DataFrame
    transformed_df = pd.DataFrame(X_transformed)

    # Write the transformed data to a new CSV file
    transformed_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    reduced(input_file, output_file)
