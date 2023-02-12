from pyecharts import options as opts
from pyecharts.charts import Map
import csv


area = []
audience = []
foreign = ['马来西亚', '美国', '英国', '新加坡', '澳大利亚', '日本', '加拿大', '新西兰', '德国', '刚果民主共和国', '', '巴西',
           '荷兰', '西班牙', '瑞典', '韩国', '法国', '摩尔多瓦', '安哥拉', '俄罗斯', '葡萄牙', '波兰', '泰国']

with open('data/comments_30000+.csv', 'r', encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)
    # print(content)
    # i = 0
    for row in content:
        # i += 1
        province = row[1]
        if (province == '西藏') or (province == '内蒙古'):
            province += '自治区'
        elif province == '新疆':
            province += '维吾尔自治区'
        elif province == '宁夏':
            province += '回族自治区'
        elif province == '广西':
            province += '壮族自治区'
        elif (province == '北京') or (province == '天津') or (province == '上海') or (province == '重庆'):
            province += '市'
        elif province == '中国香港':
            province = '香港特别行政区'
        elif province == '中国澳门':
            province = '澳门特别行政区'
        elif province == '中国台湾':
            province = '台湾省'
        else:
            province += '省'

        if province in foreign:
            continue
        if province not in area:
            area.append(province)
            audience.append(1)
        else:
            audience[area.index(province)] += 1

# print(area)
# print(audience)
# print(sum(audience))
# print(i)
# for j in range(34):
#     print(area[j], audience[j])

# pieces = [
#     {"max":800, 'min':640, 'label':'640-800', 'color':'#8A0808'},
#     {"max":640, 'min':480, 'label':'480-640', 'color':'#B40404'},
#     {"max":480, 'min':320, 'label':'320-640', 'color':'#DF0101'},
#     {"max":320, 'min':160, 'label':'160-320', 'color':'#F5A9A9'},
#     {"max":160, 'min':0, 'label':'0-160', 'color':'#FFFFF'},
# ]
c = (
    Map(init_opts=opts.InitOpts(width='1000px', height='600px'))
    .add("观影人数", [list(z) for z in zip(area, audience)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国观影人数分布"),
        visualmap_opts=opts.VisualMapOpts(max_=800, is_piecewise=True),
    )
    .render("html/audience_heatmap.html")
)
