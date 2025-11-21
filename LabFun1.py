import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

def hac_manual_correct(data, linkage='single'):
    n = data.shape[0]
    clusters = [[i] for i in range(n)]  # each point is a cluster
    distances = squareform(pdist(data))
    np.fill_diagonal(distances, np.inf)

    cluster_ids = {i: i for i in range(n)}  # map cluster to index in linkage matrix
    next_cluster_id = n  # new clusters will start at index n
    Z = []

    for _ in range(n - 1):
        # find two closest clusters
        i, j = np.unravel_index(np.argmin(distances), distances.shape)
        if j < i:
            i, j = j, i

        # record in linkage matrix: [idx1, idx2, distance, size]
        cluster_i = cluster_ids[i]
        cluster_j = cluster_ids[j]
        new_cluster = clusters[i] + clusters[j]
        Z.append([cluster_i, cluster_j, distances[i, j], len(new_cluster)])

        # update distances for the new cluster
        for k in range(distances.shape[0]):
            if k != i and k != j:
                if linkage == 'single':
                    dist = min(distances[i, k], distances[j, k])
                elif linkage == 'complete':
                    dist = max(distances[i, k], distances[j, k])
                elif linkage == 'average':
                    dist = (distances[i, k] * len(clusters[i]) + distances[j, k] * len(clusters[j])) / len(new_cluster)
                distances[i, k] = distances[k, i] = dist

        # update cluster info
        clusters[i] = new_cluster
        cluster_ids[i] = next_cluster_id
        next_cluster_id += 1

        # "remove" cluster j
        distances[j, :] = np.inf
        distances[:, j] = np.inf

    return np.array(Z)

# Example dataset
data = np.array([
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0]
])

# Compute linkage
Z_correct = hac_manual_correct(data, linkage='single')

# Plot dendrogram
plt.figure(figsize=(8, 5))
dendrogram(Z_correct, labels=[f"State {i+1}" for i in range(data.shape[0])])
plt.title("Correct Manual HAC Dendrogram")
plt.xlabel("States")
plt.ylabel("Distance")
plt.show()
