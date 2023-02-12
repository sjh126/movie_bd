import csv
from pyecharts.charts import WordCloud


frequency = {}
with open('data/words.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    # print(content)
    words = content.split()
    # print(words)
    for each in words:
        if each not in frequency.keys():
            frequency[each] = 1
        else:
            frequency[each] += 1


# print(frequency)
for each in list(frequency.keys()):
    if frequency[each] < 8:
        del frequency[each]

# print(frequency)
# print(sorted(frequency.items(), key=lambda x: x[1]))

wordCloud = WordCloud()
wordCloud.add(series_name="电影类型", data_pair=frequency.items(), word_size_range=[10, 50], mask_image='pic/TV.png')

wordCloud.render("html/comments_wordcloud.html")
#
print("success!")