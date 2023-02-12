# 根据new.csv每年的电影票房做一个统计图

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('new.csv', encoding='utf-8')

# 去掉df中时间小于2009的数据和大于2022的数据
df = df[(df['时间'] >= 2009) & (df['时间'] <= 2022)]

# 去掉票房大于58亿的数据
df = df[df['票房（万）'] < 5800000]

# 统计每年的电影票房
df1 = df.groupby('时间').sum()
# 统计国产的电影票房
df2 = df[df['国产'] == 1].groupby('时间').sum()
# 统计国外的电影票房
df3 = df[df['国产'] == 0].groupby('时间').sum()

# 绘制图形,横坐标是时间,纵坐标是电影票房
plt.plot(df1.index, df1['票房（万）'], color='red', marker='o', linestyle='solid')
plt.plot(df2.index, df2['票房（万）'], color='blue', marker='o', linestyle='solid')
plt.plot(df3.index, df3['票房（万）'], color='green', marker='o', linestyle='solid')

# 标注图例
plt.legend(['total', 'domestic', 'foreign'])

# 保存并显示图形
plt.xlabel('year')
plt.ylabel('box office')
plt.title('box office per year')
plt.savefig('box_office.png')
plt.show()
