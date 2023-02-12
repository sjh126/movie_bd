# 对comments.csv的IP地址的评论数量做一个统计图

import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示，防止label中文乱码
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# 读取数据
df = pd.read_csv('comments.csv', encoding='utf-8')

# 统计每个在中国的IP地址的评论数量
CH = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门', '台湾']
df1 = df[df['IP'].isin(CH)].groupby('IP').count()

# 绘制图形,横坐标是IP地址,纵坐标是评论数量
fig = plt.figure(figsize=(16, 9))
# IP按照评论数量从大到小排序
# plt.bar(df1.index, df1['评论'])
plt.bar(df1.sort_values(by='评论', ascending=False).index, df1.sort_values(by='评论', ascending=False)['评论'])
# plt.tick_params(axis='x', labelsize=8)
plt.xticks(rotation=-15)
# 保存并显示图形
plt.xlabel('IP地址')
plt.ylabel('评论数量')
plt.title('评论数在IP地址上的分布')
plt.savefig('IP.png')
plt.show()
