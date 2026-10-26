from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import spectral_clustering
from sklearn.metrics import silhouette_score
from itertools import cycle

# 读取数据
file_path = "D:\\Ctoo\\Project_xinyang\\Project_xinyang\\XLL2.xlsx"
df = pd.read_excel(file_path, index_col=0)
similarity_matrix = df.values

# 定义一个函数来计算不同簇数下的轮廓系数
def calculate_silhouette_score(similarity_matrix, cluster_range):
    silhouette_scores = []
    for n_clusters in cluster_range:
        labels = spectral_clustering(similarity_matrix, n_clusters=n_clusters, assign_labels='discretize')
        silhouette_avg = silhouette_score(similarity_matrix, labels)
        silhouette_scores.append(silhouette_avg)
    return silhouette_scores

# 定义簇数范围
cluster_range = range(2, 11)  # 例如，从2到10个簇

# 计算轮廓系数
silhouette_scores = calculate_silhouette_score(similarity_matrix, cluster_range)

# 绘制手肘图
plt.figure()
plt.plot(cluster_range, silhouette_scores, 'bx-')
plt.xlabel('Estimated number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Scores for Different Numbers of Clusters')
plt.show()

# 选择轮廓系数最高的簇数
optimal_clusters = cluster_range[np.argmax(silhouette_scores)]
print(f"Optimal number of clusters: {optimal_clusters}")

# 使用最优簇数重新聚类
labels = spectral_clustering(similarity_matrix, n_clusters=optimal_clusters, assign_labels='discretize')

# 绘制聚类结果
n_samples = len(df)
perplexity = min(50, n_samples - 1)  # 设置 perplexity 为样本数减一，但不超过 50
tsne = TSNE(n_components=2, perplexity=perplexity)
embedded_data = tsne.fit_transform(similarity_matrix)
plt.figure(1)
plt.clf()
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(optimal_clusters), colors):
    my_members = labels == k
    cluster_center = np.mean(embedded_data[my_members], axis=0)
    plt.plot(embedded_data[my_members, 0], embedded_data[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'kX', markersize=12)
plt.title('Estimated number of clusters: %d' % optimal_clusters)
plt.show()

# 使用该字典创建一个新的DataFrame
cluster_dict = dict(zip(df.index, labels))

# 将新的DataFrame导出到Excel文件
output_path = "D:\\Ctoo\\Project_xinyang\\clustered_cities.xlsx"
cluster_df = pd.DataFrame(list(cluster_dict.items()), columns=['City', 'Cluster_Label'])
cluster_df.to_excel(output_path, index=False) 

print(f"导出 {output_path}")