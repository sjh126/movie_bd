# 对new.csv的每年的电影的平均评分做一个统计图

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('new.csv', encoding='utf-8')

# 去掉df中时间小于2009的数据和大于2022的数据
df = df[(df['时间'] >= 2009) & (df['时间'] <= 2022)]

# 统计每年的电影平均评分
df1 = df.groupby('时间').mean()
# 统计国产的电影平均评分
df2 = df[df['国产'] == 1].groupby('时间').mean()
# 统计国外的电影平均评分
df3 = df[df['国产'] == 0].groupby('时间').mean()

# 绘制图形,横坐标是时间,纵坐标是电影平均评分
plt.plot(df1.index, df1['评分'], color='red', marker='o', linestyle='solid')
plt.plot(df2.index, df2['评分'], color='blue', marker='o', linestyle='solid')
plt.plot(df3.index, df3['评分'], color='green', marker='o', linestyle='solid')

# 标注图例
plt.legend(['total', 'domestic', 'foreign'])

# 保存并显示图形
plt.xlabel('year')
plt.ylabel('average score')
plt.title('average score per year')
plt.savefig('score.png')
plt.show()
