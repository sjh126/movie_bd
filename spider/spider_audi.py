import requests
import re
import os
import pandas as pd
import time as tm
from time import sleep
import sqlite3
from lxml import etree # 提取信息库
from bs4 import BeautifulSoup
import json #引用json
# 日期
today = tm.strftime('%Y{y}%m{m}%d{d}',tm.localtime()).format(y='年',m='月',d='日')
cookie = '''ll="118268"; bid=dkIK8qCmkiw; __yadk_uid=r7kiBkZMjuVE48jLHGcT8fxoaUlTTtpM; __gads=ID=1f67bc9c700459f8-226bc5cf28d90018:T=1672578921:RT=1672578921:S=ALNI_Ma8WDbFWRSc1MrZWa4S7tcfi2OEvw; _vwo_uuid_v2=D4FF390B9A2119C07204C07A7BA9F31B1|eb957af0cbc07fc464b7be914b05728d; ct=y; __utmc=30149280; __utmc=223695111; __utmz=223695111.1675486543.12.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/doulist/46436333/; __utmz=30149280.1675490951.18.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/35267208/comments; _pk_ref.100001.4cf6=["","",1675495803,"https://www.douban.com/doulist/46436333/"]; _pk_ses.100001.4cf6=*; __utma=30149280.757314036.1672578921.1675490951.1675495804.19; __utma=223695111.529519264.1672578921.1675490957.1675495815.15; __utmb=223695111.0.10.1675495815; push_doumail_num=0; push_noty_num=0; dbcl2="267365034:a1GFHEiwQbQ"; ck=GLaj; __utmv=30149280.26736; frodotk_db="f6ac4715637a866ee404d5402a6f934a"; __gpi=UID=00000b9bb6c56ec4:T=1672578921:RT=1675498321:S=ALNI_MY1fDMNnj4mr5-aMOAP1DWR1ZL3TQ; __utmb=30149280.22.10.1675495804; _pk_id.100001.4cf6=95ddde700907f914.1672578920.15.1675498468.1675492380.'''
headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    ,'Cookie': cookie
}
select_headers = { #新增爬电影用url
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    ,'Cookie': cookie
    ,'Referer': 'https://movie.douban.com/explore'
    ,'Host':'m.douban.com'
    ,'Origin':'https://movie.douban.com'
}
'''
obj = re.compile(r'<a href="(?P<href>.*?)" class="">(?P<id>.*?)</a>')
obj_rating = re.compile(r'allstar(?P<rating>.*?)0')
obj_ip = re.compile(r'location">(?P<ip>.*?)</span>')
obj_comments =re.compile(r'<span class="short">(?P<comments>.*?)</span>' , re.S)
'''
obj_rating = re.compile(r'allstar(?P<rating>.*?)0')
id_re=re.compile(r'>.*<')
web_re=re.compile(r'"https.+"')
#re.compile(r'class="comment-info">/<a href="(?P<href>.*?)" class="">'
       #         , re.S)

#obj_menu = re.compile(r'<br/>[内內]地票房年度[总總]排行：(?P<year>.*?)年(电影|電影) .*?">(?P<domain_pre>.*?)<wbr/>'
 #                     r'(?P<domain_suffix>.*?)(<wbr/>|</a>)', re.S)

df = pd.DataFrame()
href = []
rating = []
name = []
ip = []
comments = []
cnt = 1
def bug_catch(url):
    global cnt
    comments_cnt = 0
    for j in range(0, 25):
        sleep(2)
        new_url = url + "?start=" + str(20 * j)+"&limit=20&status=P&sort=new_score"
        #print("正在爬取 "+new_url)
        res = requests.get(new_url, headers=headers)
        
        soup = BeautifulSoup(res.text, 'lxml')#使用bs4解析
        onepiece = soup.select(#将每条评论分割开
            '#comments > div ')
        for item in onepiece:#对每一条数据解析
            #print(item)
            place_line=item.select('div.comment > h3 > span.comment-info > span.comment-location')
            id_line=item.select(' div.comment > h3 > span.comment-info > a')
            scoreblock=item.select('div.comment > h3 > span.comment-info')
            score=114514
            if scoreblock !=[]:#处理没有打分的情况
                score=obj_rating.search(str(scoreblock[0]))
                if (score != None):
                    score=str(score[0])[7:-1]
            comment=item.select('div.comment > p > span')
            if (id_line ==[]):#跳过末尾的非用户信息
                continue
            #从html中截取需要部分
            place=str(place_line[0])[31:-7]
            id=str(id_re.search(str(id_line))[0])[1:-1]
            web=web_re.search(str(id_line[0])).group()[1:-1]
            comment=str(comment[0])[20:-7]
            #------------------------------------------------调试用输出，从上到下依次是用户名，个人主页网址，打分（5分制，没打分默认114514),ip地址，短评
            name.append(id)
            ip.append(place)
            rating.append(score)
            comments.append(comment)
            href.append(web)
        comments_cnt=len(ip)
    print('cnt =',cnt , " coments_cnt =" ,comments_cnt)
    cnt+=1
    sleep(2)

def select(url):   #在 选电影 页面获取电影的id以备work函数使用
    res = requests.get(url, headers=select_headers)
    data=json.loads(res.text)
    data=data['items']
    for flim in data:
        sleep(2)
        flim_id=flim['id']
        comments_url='https://movie.douban.com/subject/'+str(flim_id)+'/comments'
        bug_catch(comments_url)


def main():
    print("请稍等......")

    #resp_content = requests.get("https://movie.douban.com/subject/35267208/comments",headers=headers).text
    #content = obj_menu.finditer(resp_content)
    select("https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=0&count=20&selected_categories=%7B%22%E5%9C%B0%E5%8C%BA%22:%22%E5%8D%8E%E8%AF%AD%22%7D&uncollect=false&tags=%E5%8D%8E%E8%AF%AD&ck=GLaj")
    select("https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=20&count=20&selected_categories=%7B%22%E5%9C%B0%E5%8C%BA%22:%22%E5%8D%8E%E8%AF%AD%22%7D&uncollect=false&tags=%E5%8D%8E%E8%AF%AD&ck=GLaj")
    select("https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=40&count=20&selected_categories=%7B%22%E5%9C%B0%E5%8C%BA%22:%22%E5%8D%8E%E8%AF%AD%22%7D&uncollect=false&tags=%E5%8D%8E%E8%AF%AD&ck=GLaj")
    '''
    for it in content:
        print("读取到数据"+it.group("year")+" : "+it.group("domain_pre") + it.group("domain_suffix"))
        bug_catch(it.group("year"),it.group("domain_pre") + it.group("domain_suffix"))
    '''
    df['用户名'] =  name
    df['IP'] =  ip
    df['主页网址'] = href
    df['评分'] =  rating
    df['评论']= comments
    df.to_csv('comments.csv',mode='w',index=None,encoding='utf-8')
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