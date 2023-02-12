import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.manifold import TSNE

df=pd.read_csv('data/mvs.csv')
data=df.values
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data)

marker=[]
fh=['.','v','^','<','>','8','s','p','*','h','H','+','x']
color=['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']
n_clusters=5
#for n_clusters in range(8):
#    if n_clusters<=1:
#        continue
cluster = KMeans(n_clusters=n_clusters,random_state=0).fit(data)
centroid=cluster.cluster_centers_
y_labels=cluster.labels_
# print('-----------------------------------',   list(set(y_labels)))
print('n=',n_clusters,'CH:',metrics.calinski_harabasz_score(data,y_labels))
print(metrics.silhouette_score(data,y_labels))

tsne = TSNE(n_components=2)
x_tsne=tsne.fit_transform(data)
plt.figure(figsize=(10, 5))
j=0
for i in range(1743):
    plt.scatter(x_tsne[j, 0], x_tsne[j, 1], c=color[y_labels[j]],marker=fh[0])
    j+=1
plt.legend()
plt.show()


# import pyecharts.options as opts
# from pyecharts.charts import Scatter
# x = [[], [], [], [], []]
# y = [[], [], [], [], []]
#
# for j in range(1743):
#     x[y_labels[j]].append(x_tsne[j, 0])
#     y[y_labels[j]].append(x_tsne[j, 1])
#
# print(x[0])
# print(y[0])
#
# # scatter = Scatter()
# # scatter.add_xaxis(xaxis_data=x[0])
# # scatter.add_yaxis("", y_axis=y[0])
# # # scatter.add_xaxis(xaxis_data=x[1])
# # # scatter.add_yaxis("", y_axis=y[1])
# # scatter.render("scatter.html")
# (
#     Scatter()
#     .add_xaxis(xaxis_data=x[0])
#     .add_yaxis(
#         series_name="",
#         y_axis=y[0],
#         symbol_size=20,
#         label_opts=opts.LabelOpts(is_show=False),
#     )
#     .set_series_opts()
#     .set_global_opts(
#         xaxis_opts=opts.AxisOpts(
#             type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
#         ),
#         yaxis_opts=opts.AxisOpts(
#             type_="value",
#             axistick_opts=opts.AxisTickOpts(is_show=True),
#             splitline_opts=opts.SplitLineOpts(is_show=True),
#         ),
#         tooltip_opts=opts.TooltipOpts(is_show=False),
#     )
#     .render("basic_scatter_chart.html")
# )




