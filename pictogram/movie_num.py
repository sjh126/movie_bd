# 对new.csv的每年的电影数量做一个统计图

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('new.csv', encoding='utf-8')

# 去掉df中时间小于2009的数据和大于2022的数据
df = df[(df['时间'] >= 2009) & (df['时间'] <= 2022)]

# 统计每年的电影数量
df1 = df.groupby('时间').count()
# 统计国产的电影数量
df2 = df[df['国产'] == 1].groupby('时间').count()
# 统计国外的电影数量
df3 = df[df['国产'] == 0].groupby('时间').count()

# 绘制图形,横坐标是时间,纵坐标是电影数量
plt.plot(df1.index, df1['电影名称'], color='red', marker='o', linestyle='solid')
plt.plot(df2.index, df2['电影名称'], color='blue', marker='o', linestyle='solid')
plt.plot(df3.index, df3['电影名称'], color='green', marker='o', linestyle='solid')

# 标注图例
plt.legend(['total', 'domestic', 'foreign'])

# 保存并显示图形
plt.xlabel('year')
plt.ylabel('number')
plt.title('number of movies per year')
plt.savefig('movie_num.png')
plt.show()
