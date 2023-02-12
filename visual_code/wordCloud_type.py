import csv
from pyecharts.charts import WordCloud

frequency = {}
with open('data/new.csv', 'r', encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)
    # print(content)
    for row in content:
        label = row[3].split(" / ")
        for ty in label:
            if ty not in frequency.keys():
                frequency[ty] = 1
            else:
                frequency[ty] += 1

# print(frequency)
wordCloud = WordCloud()
wordCloud.add(series_name="电影类型", data_pair=frequency.items(), word_size_range=[20, 80])

wordCloud.render("html/type_wordcloud.html")

print("success!")
# print(sorted(frequency.items(), reverse= True, key = lambda x: x[1]))
