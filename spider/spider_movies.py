import requests
import re
import pandas as pd
import time as tm
from time import sleep
import sqlite3
# 日期
today = tm.strftime('%Y{y}%m{m}%d{d}',tm.localtime()).format(y='年',m='月',d='日')

headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    
}
obj = re.compile(r'ic_play_web@2x.png"/>(?P<film_name>.*?)</a>.*?rating_nums">(?P<rating>.*?)</span>'
                 r'.*?类型: (?P<kind>.*?)<br />.*?制片国家/地区: (?P<area>.*?)<br />.*?【.*?】(?P<time>.*?)开画.*?累计票房(?P<total_price>.*?)元', re.S)

obj_menu = re.compile(r'<br/>[内內]地票房年度[总總]排行：(?P<year>.*?)年(电影|電影) .*?">(?P<domain_pre>.*?)<wbr/>'
                      r'(?P<domain_suffix>.*?)(<wbr/>|</a>)', re.S)

df = pd.DataFrame()
film_name = []
rating = []
kind = []
area = []
time = []
total_price = []

def bug_catch(file_name,url):
    '''
    table_name = "film_info_" + file_name
    # 创建数据表
    c.execute(CREATE TABLE if not exists %s (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 film_name TEXT NOT NULL,
                                 rating TEXT,
                                 kind TEXT,
                                 time TEXT,
                                 total_price TEXT)
             % table_name)
    conn.commit()
    '''
    #f = open(file_name+".csv", "w")
    #csvwriter = csv.writer(f)
    for j in range(0, 6):
        new_url = url + "?start=" + str(25 * j)
        print("正在爬取 "+new_url)
        resp = requests.get(new_url, headers=headers)
        page_content = resp.text
        content = obj.finditer(page_content)

        for i in content:
            dic = i.groupdict()
            #print(dic)
            film_name.append(dic['film_name'].strip())
            rating.append(dic['rating'].strip())
            kind.append(dic['kind'].strip())
            area.append(dic['area'].strip())
            time.append(dic['time'].strip())
            total_price.append(dic['total_price'].strip())
            #print(film_name)
            '''
            dic['rating'] = dic['rating'].strip()
            dic['kind'] = dic['kind'].strip()
            dic['time'] = dic['time'].strip()
            dic['total_price'] = dic['total_price'].strip()
            '''
        #    sql = '''INSERT INTO %s (film_name,rating,kind,time,total_price) 
        #           values('%s','%s','%s','%s','%s')''' % (table_name,dic['film_name'],dic['rating'],
        #                                                   dic['kind'],dic['time'],dic['total_price'])
        #    c.execute(sql)
        #    conn.commit()

        sleep(2)
        #resp.close()

def main():
    print("请稍等......")

    resp_content = requests.get("https://www.douban.com/doulist/148892322/",headers=headers).text
    content = obj_menu.finditer(resp_content)
    
    for it in content:
        print("读取到数据"+it.group("year")+" : "+it.group("domain_pre") + it.group("domain_suffix"))
        bug_catch(it.group("year"),it.group("domain_pre") + it.group("domain_suffix"))
    
    bug_catch("2022","https://www.douban.com/doulist/148892322/")
    df['电影名称'] =  film_name
    df['评分'] =  rating
    df['类型'] =  kind
    df['制片国家/地区'] = area
    df['时间'] = time
    df['票房'] = total_price
    df.to_csv('电影'+today+'.csv',mode='w',index=None,encoding='utf-8')
    print('保存完成!') 
    # bug_catch("2021","https://www.douban.com/doulist/135651096/")
    # bug_catch("2020","https://www.douban.com/doulist/123308712/")
    # bug_catch("2019","https://www.douban.com/doulist/111687014/")
    # bug_catch("2018","https://www.douban.com/doulist/46436333/")
    # bug_catch("2017","https://www.douban.com/doulist/45837913/")
    # bug_catch("2016","https://www.douban.com/doulist/42975662/")
    # bug_catch("2015","https://www.douban.com/doulist/37815319/")
    # bug_catch("2014","https://www.douban.com/doulist/3401345/")
    # bug_catch("2013","https://www.douban.com/doulist/1765813/")
    # bug_catch("2012","https://www.douban.com/doulist/943009/")
    # bug_catch("2011","https://www.douban.com/doulist/665041/")
    # bug_catch("2010","https://www.douban.com/doulist/226207/")
    # bug_catch("2009","https://www.douban.com/doulist/226734/")


if __name__ == "__main__":
    main()