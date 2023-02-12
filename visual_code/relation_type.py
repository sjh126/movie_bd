from efficient_apriori import apriori
import csv
from fpgrowth_py import fpgrowth
from pyecharts import options as opts
from pyecharts.charts import Graph

wordlist = []
with open('data/new.csv', 'r', encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)
    # print(content)
    for row in content:
        label = row[3].split(" / ")
        print(len(label))
        if len(label) > 1:
            wordlist.append(label)


# sets, rules = apriori(wordlist, min_support=0.05, min_confidence=0.4)
sets,rules=fpgrowth(wordlist,minSupRatio=0.05,minConf=0.4)
print(rules)
print(len(rules))
# print(sets)


links = []
for each in rules:
    # print(each)
    if len(each[0]) == 1 and len(each[1]) == 1:
        links.append({"source": str(each[0])[2:4], "target": str(each[1])[2:4]})


links.remove({'source': '冒险', 'target': '动画'})
# print(node)
# print(len(rules[5][0]))
# print((rules[5][0]))
print(links)
print(len(links))

# ('剧情', 640), ('喜剧', 571), ('动作', 556),
# ('冒险', 440), ('爱情', 372), ('动画', 308),
# ('奇幻', 278),# ('犯罪', 220), ('科幻', 202), ('惊悚', 193), ('悬疑', 190)
nodes = [
    {"name": "剧情", "symbolSize": 110},
    {"name": "喜剧", "symbolSize": 110},
    {"name": "动作", "symbolSize": 110},
    {"name": "冒险", "symbolSize": 80},
    {"name": "爱情", "symbolSize": 80},
    {"name": "动画", "symbolSize": 80},
    {"name": "奇幻", "symbolSize": 50},
    {"name": "犯罪", "symbolSize": 50},
    {"name": "科幻", "symbolSize": 50},
    {"name": "惊悚", "symbolSize": 50},
    {"name": "悬疑", "symbolSize": 50},
]

c = (
    Graph()
    .add("", nodes, links, repulsion=8000)
    .set_global_opts(title_opts=opts.TitleOpts(title="电影类型关联关系"))
    .render("html/type_relationGraph.html")
)
