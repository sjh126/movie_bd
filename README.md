# 电影行业大数据技术报告
## 1 课题背景及意义
随着全球经济的快速发展，不同文化之间的交流也越来越频繁，文化产业自身创造的经济价值也渐渐得到了每个国家的重视，成为了一个国家重要的经济支柱，文化软实力也成为了衡量一个国家经济综合实力的重要尺度。电影产业作为文化产业的支柱性产业，承担着促进经济增长和社会和谐的重要使命。电影产业的发展对周边产业产生了很好的辐射和带动作用,助推和产生了新的经济增长点，成为促进中国经济增长的助推器。
近年来，在全球经济增长普遍放缓、国内经济下行压力加大的大背景下，我国的电影市场遇冷，一些过热的资本也逐步退出了电影行业，且从2017年起，我国电影市场票房增幅也逐年减少。虽然业内普遍认为中国电影开始进入了“冷静期”，然而2019年，中国电影却做出了令人满意的成绩，不仅市场总票房取得642.66亿元的好成绩，观众满意度也表现优秀。主要电影档期表现尤为突出，拉动了全年票房的增长，甚至国产电影在中国市场有六成以上的占有率，并加大步伐拓展海外市场。电影的工业化水平、科技水平、艺术创新能力都有了很大的提高。这些现象表明了我国电影开始向高质量发展。但是问题也是显而易见的，高票房、口碑好的电影在电影总产量中只占少数，两极分化明显，国产电影的质量还需更加全面的提升，电影产业链条仍需进一步发展完善、合理布局。然而，2020年初，新冠肺炎在全球范围内流行开来，据美国好莱坞提供的数据，这次疫情对全球影业的影响将会造成超过50亿美元的损失，多个国家的电影产业相继进入停滞发展的状态。中国有5000家大小影视相关的公司倒闭，光万达影业就亏损6个亿。虽然政府及时对电影产业相关企业提供了补贴和减免的相关政策措施，但对于电影产业自身仍旧要考虑如何调整产业结构、如何利用互联网在疫情期间保证自身的发展。
本次大作业利用大数据对往年电影行业的相关数据进行收集整理并利用可视化的方式展现出来，得到一些结论，并为电影行业发展提供简单的数据支撑。

## 2 技术路线
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/technology_roadmap.png)

## 3 数据采集

### 3.1 爬虫流程
根据小组讨论的结果，最终决定在豆瓣电影网上爬取了2009年-2022年国内上映电影的数据以及部分影片影评的观众数据。简单来说就是编写自动化脚本模拟用户向服务器发送请求GET得到返回的HTML，通过对返回页面的的分析处理从而提取所需信息。

#### 3.1.1 确定爬取网址
对于爬取电影数据来说，一开始所想的是在豆瓣搜索页(/explore)进行筛选信息之后再进行爬取。但是过程中遇到了问题，虽然网页上面有内容显示但最终却无法爬取到内容，尽管标签定位都是正确的。最后得知该网站是异步加载的数据，若要进行爬取，需要先找到存放数据的json。而其他排行页等数据都是同步加载的数据，于是可以直接利用豆瓣网统计内地电影排行榜的网站进行爬取。
对于观众影评数据，不用多说，就是电影详情短评页。
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/pic_2.png)

#### 3.1.2 获取网页HTML源码
接着编写代码用确定的url以及requests.get()方法来获取页面的text。之后可用分词或者xpath来获取可用信息。

#### 3.1.3 分析数据并保存内容
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/pic_3.png)

### 3.2反反爬虫
很多网站都有反爬虫限制机制，例如上面提到的异步js，已经被绕过。为了避免针对访问频率限制的反爬虫，我们在这里采用sleep的方式随机化访问频率，从而避免访问速度过快。对于针对IP限制，可以准备好大量的替代IP，也可以使用动态IP，相较于准备大量静态ip，使用动态ip的效率会更高。
我们使用requests库登录豆瓣，因为豆瓣在没有登录状态情况下只允许查看前200条影评，想要查看更多内容就需要登录才能查看，这也算是一种反爬手段。针对这个问题可以利用登录后的cookie进行解决。
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/pic_4.png)

## 4 数据清洗
针对获取到的电影信息，首先需要整理爬虫得到原始数据，进行去除错误、统一单位的工作。如原始数据的“票房”部分存在“万”“亿”混用的问题，有些位置因为网络原因有大量无效信息，这些错误都会给后续的数据分析工作带来不利的影响。幸运的是，可以使用正则匹配等手段解决。接下来需要完成的工作是特征的提取，很多原始信息并不适合直接使用，如日期过于详细，制片地址五花八门，电影类型全都挤在一起等。针对这些问题，我们分别采取了缩减日期为年份、区分国产和分离类型的方式，通过创建新的二元属性来标定电影是否国产、是否具有某种类型，为后续分析打好基础。最后，还对所有信息进行了标准化，排除了数值大小对结果的影响。
在爬虫获取到的评论信息中，评论都是一个个句子，显然不适用于各种分析算法，因此首先需要进行分词。分词选用了python的结巴库，配合停用词表，就可以方便地提取出每一句的重要词了。

## 5 数据加工与大数据分析算法
在hadoop编程中，主要使用了三种方式进行数据分析。首先是单词计数，这也是hadoop编程中最经典的例子，能够辅助我们了解词语出现的频率和趋势。它利用map阶段将每一句的词语划分后放入key，在reduce阶段将相同词语的出现频率累加起来，最终实现词频的统计功能。
接着，我们还使用了hadoop环境下的关联规则挖掘，采用了并行化的fpgrowth算法。为了完成挖掘，需要进行三轮hadoop运算。首先，需要进行一轮wordcount，获取各个词语的词频，并剔除显然不达标的词。接着，使用词频信息和语句信息再进行一轮hadoop，先对词频降序排序，再在map阶段对每一个句子使用排序后的词频序列进行匹配，输出句子的key和匹配到词语。句子的key可以直接使用句子本身代替，因为每个人的短评肯定都是不同的，不会出现完全相同的情况。在reduce阶段，将每个句子对应的短语整合到一起，这样实际上就完成了fp树构建前的准备工作。最后再进行一次hadoop，在reduce阶段构建树并完成规则的挖掘工作。
最后，我们还在hadoop上进行了数据的聚类操作。与前两个分析不同，我们对电影信息而非评论信息进行聚类，输入采用数据清洗后得到的电影数据。聚类的大致思路是利用一遍hadoop过程实现kmeans算法的一次迭代，在map阶段利用上一轮已知的质心坐标对所有点进行重新划分，将划分结果的编号和点的特征向量分别作为key和value传入reduce阶段。在reduce阶段利用传入的value信息，重新计算key编号的质心坐标向量并写入。在每进行完一轮后，对新老结果进行比较并用新结果覆盖老结果，不断循环直到满足要求或达到上限次数时终止。

## 6 可视化

### 6.1直接数据可视化展示
在本部分内容中，我们通过对经过数据清洗后的数据在单列单维度上进行了可视化的展示（采用pandas和matplotlib)，从而获取到一些关于电影数据以及用户评论数据的简单统计，最终得到了一些比较明显的简单结论。

#### 6.1.1 电影数据展示
（1）每年的电影数量统计（总共，国内，国外）
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/movie_num.png)
总体来看，09年到19年电影数量在逐步增长，其中09到14年比较稳定，15年到19年由于可能的政策等影响在国产和国外引进的电影的倾向方面有所波动。直到20年疫情爆发，电影行业受到冲击，后面两年呈现颓势。可能在疫情结束后才会重新回暖。
（2）每年的电影票房（总共，国内，国外；单位:万）
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/box_office.png)
总体来看，09年到14年电影票房激增，电影行业迅速发展，15年到19年增势渐缓，行业发展减缓；直到20年疫情爆发，电影行业受到冲击，后面两年不可避免的票房下降。可能在疫情结束后才会重新回暖。
（3）每年电影的平均评分
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/score.png)
总体来看，国外引进的电影评分明显高于国产电影，毕竟引进时是经过筛选的，而国产电影相对来说标准还是低了一点，也能够理解。
（4）三图结合分析得到结论：
在整体电影占比中，国产电影比重较大，但在电影产业发展初期，国产电影票房和非国产电影差距并不大，同时评分也是非国产电影更高，也就是说电影行业发展前期，国产电影还是存在较大问题。而在后面发展中，国产电影票房逐渐与非国产电影拉开差距，而电影占比反而波动不大，也就是说国产电影也在逐渐变好，电影行业也在不断发展。虽然受到20年疫情的冲击，电影行业发展有所停滞，但在解除疫情管控的今后，我们应当相信电影行业也会回暖，重新释放生机。

#### 6.1.2 电影评论数量的IP分布
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/IP.png)
从ip分布来看，发达地区往往更喜欢发表影评，虽然还有其它因素影响，但也基本反应了当生活水平提高，物质层面得到满足后，人们开始追求精神层面的享受，电影就是其中的一种方式。

### 6.2 大数据分析算法结果
在本部分内容中，我们通过对经过加工以及大数据算法分析后的数据进行可视化结果展示（采用pyecharts），进一步对内容进行分析，最终得到较为可靠的结论。

#### 6.2.1 热力图
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/heat_map.png)
通过热力图我们能够很明显的得到中国观影人数的分布，与地区发达程度有所关联，北京作为我国首都在观影人数上的领先程度也是比较明显。热力图结果也可以与前面直接数据展示的ip分布相互论证。

#### 6.2.2 基于词频计算的词云
（1）电影类型词云
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/wordcloud1.png)
（2）影评词云
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/wordcloud2.png)

#### 6.2.3 电影类型的数量及所占比例的变化
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/proportion1.png)
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/proportion2.jpg)
从图中可以看出历年来喜剧和爱情种类的电影占比较大，虽然有所波动但仍旧占据大头；惊悚类电影随着时间过度占比逐渐减小，不再受大众喜爱；动画和奇幻题材的电影随着时间变化占比有所增加，也能够看出国产动画电影的进步；其它题材的电影虽然有所波动而且变化不够明显，但仍是重要的电影类型组成。

#### 6.2.4 kmeans聚类结果降维展示
我们将大数据分析后的聚类结果使用降维后进行染色并展示：
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/k-means.png)

#### 6.2.5关联规则挖掘结果展示
![image](https://github.com/sjh126/movie_bd/blob/pic-mv/rules.png)

## 7 结果论证
通过对豆瓣网站上的历年电影相关信息以及部分电影的评论信息进行大数据的分析总结得到了下面的结论：
(1)电影行业20年之前的几年来电影数量以及总票房都在增加，也意味这中国电影行业的不断发展。虽然20年疫情出现，各地实行封闭管控使得当年的影片数量及票房骤降，电影行业受到打击，但随着疫情管控的逐渐放开，电影行业的状况也逐渐回暖，焕发新的生机。
(2)国产电影的电影类型也在随着行业发展不断更新，剧情、喜剧、动作这三种题材占据电影总比的大头，虽然具体比重有所波动，但整体依旧强势；惊悚类占比的逐渐降低以及动画、奇幻类型电影的比重增加，也显示着观众口味的变化以及行业发展的改变。
(3)人们对于电影的要求也逐渐增高，用户讨论最多的是剧情方面，而剧情也是一部电影好坏评价的关键，对一部电影的整体评分有着重要影响。其他方面关于导演、演员以及演员的演技、还有电影的题材也是用户讨论的组成部分，同样影响着对于一部电影的总体评价。
