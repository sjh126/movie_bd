import csv
import pyecharts.options as opts
from pyecharts.charts import ThemeRiver

frequency = {}
x_data = ['剧情', '喜剧', '动作', '冒险', '爱情', '动画', '奇幻', '犯罪', '科幻', '惊悚', '悬疑']
y_data = []


for kind in x_data:
    # print(kind)
    with open('data/new.csv', 'r', encoding='utf-8') as file:
        content = csv.reader(file)
        header = next(content)
        # print(content)
        dic = {}
        for row in content:
            if row[7] == "0.0":
                continue
            label = row[3].split(" / ")
            if kind in label:
                if row[5] not in dic.keys():
                    dic[row[5]] = 1
                else:
                    dic[row[5]] += 1
    for key, value in dic.items():
        # value /= year_num[key]
        y_data.append([key, value, kind])
    # for each in y_data:
    #     print(each)

year_num = {}
for each in y_data:
    if each[0] not in year_num.keys():
        year_num[each[0]] = each[1]
    else:
        year_num[each[0]] += each[1]

for each in y_data:
    each[1] /= year_num[each[0]]

print(y_data)

# print("-----------------------------0-------------")

# print(y_data)
# for each in y_data:
#     print(each)

(
    ThemeRiver()
    .add(
        series_name=x_data,
        data=y_data,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"
        ),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
    )
    .render("html/type_theme_river.html")
)


