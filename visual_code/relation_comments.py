from fpgrowth_py import fpgrowth
from pyecharts import options as opts
from pyecharts.charts import Graph

f=open('data/words.txt','r',encoding='utf-8')
key_word = ['剧情', '导演', '喜欢', '感觉', '人物', '演员', '喜剧', '不错', '角色', '好看', '观众', '演技', '尴尬', '情节', '台词',
            '希望', '搞笑', '镜头', '爱', '影片', '剧本']
mkey = ['剧情', '导演', '角色', '演员', '编剧', '结尾', '国产', '题材']
wordlist=[]
line=f.readline()
while True:
    if line:
        oneline=line.split()
        for each in mkey:
            if each in oneline:
                l = oneline.index(each)
                t = []
                for i in range(3):
                    if l - i >= 0:
                        t.append(oneline[l - i])
                    else:
                        break
                for i in range(4):
                    if l + i < len(oneline):
                        t.append(oneline[l + i])
                    else:
                        break
                wordlist.append(t)
        line=f.readline()
    else:
        break

sets,rules=fpgrowth(wordlist,minSupRatio=0.005,minConf=0.5)
print(rules)
print(len(rules))
# print(wordlist)

# for each in rules:
#     print(rules.index(each), each)

select = [1, 2, 4, 6, 7, 8, 9, 13, 19, 23, 25, 27, 31, 33, 35, 39]
new = []
for each in rules:
    # print(rules.index(each), each)
    if rules.index(each) in select:
        new.append(each)

# for each in new:
#     print(new.index(each), each)

# print(str(new[3][0])[2:-2])
s = ['国产', '剧情', '导演', '题材', '角色', '演员']
links = []
for each in s:
    links.append({"source": '电影', "target": each})
links.append({"source": '导演', "target": '风格'})
for each in new:
    # print(each)
    t = {"source": str(each[0])[2:-2], "target": str(each[1])[2:-2]}
    if t not in links:
        links.append(t)

# print('--------------------------------', len(links))
for each in links:
    print(each)

nodes = [
    {"name": "电影", "symbolSize": 140},
    {"name": "剧情", "symbolSize": 100}, #     ---------------- 100
    {"name": "科幻", "symbolSize": 60}, #489
    {"name": "国产", "symbolSize": 80}, #718  ---------------- 80
    {"name": "紧凑", "symbolSize": 50},  #162
    {"name": "处女作", "symbolSize": 50},  #17
    {"name": "导演", "symbolSize": 100},  #    ---------------- 100
    {"name": "风格", "symbolSize": 55},  #    ---------------- 100
    {"name": "现实", "symbolSize": 60},   #651
    {"name": "题材", "symbolSize": 80},   #770 ----------------  80
    {"name": "水平", "symbolSize": 50},   #367
    {"name": "笑点", "symbolSize": 60},   #702
    {"name": "简单", "symbolSize": 50},   #409
    {"name": "在线", "symbolSize": 50},   #205
    {"name": "演技", "symbolSize": 60},   #1437 ------------80
    {"name": "塑造", "symbolSize": 50},   #409
    {"name": "角色", "symbolSize": 90},   #1596 ---------------- 90
    {"name": "作品", "symbolSize": 60},   # 833
    {"name": "逻辑", "symbolSize": 60},   # 698
    {"name": "特效", "symbolSize": 60},    #819
    {"name": "节奏", "symbolSize": 60},    #983
    {"name": "女性", "symbolSize": 60},    #690
    {"name": "动画", "symbolSize": 60},    #648
    {"name": "演员", "symbolSize": 90},    #1701 ---------------- 90
]

c = (
    Graph(init_opts=opts.InitOpts(width='1000px', height='600px'))
    .add("", nodes, links, repulsion=5000)
    .set_global_opts(title_opts=opts.TitleOpts(title="电影评论关联关系"))
    .render("html/comment_relationGraph.html")
)
# ('演技', 1437), ('观众', 1510), ('挺', 1530), ('好看', 1590), ('角色', 1596), ('不错', 1692), ('喜剧', 1698),
# ('演员', 1701), ('人物', 1974), ('感觉', 1983), ('喜欢', 2194), ('导演', 2412), ('剧情', 2626)]

# ('尴尬', 899), ('世界', 900), ('真', 900), ('一点', 904), ('情节', 911), ('台词', 932), ('讲', 938), ('希望', 940),
# ('搞笑', 951), ('镜头', 973), ('节奏', 983), ('结尾', 1009), ('爱', 1027), ('画面', 1044), ('表演', 1059), ('影片', 1078),
# ('煽情', 1106), ('戏', 1118), ('哭', 1198), ('剧本', 1214),