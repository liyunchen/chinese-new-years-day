# -*- coding: utf-8 -*-

## 李运辰 2021-2-15

import requests
import jieba
from stylecloud import gen_stylecloud
from lxml import etree
import xlrd
import xlwt
import time
import random
from xlutils.copy import copy
import matplotlib as mpl
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# matplotlib中文显示
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

headers = {
            'Host':'movie.douban.com',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
            'cookie':'bid=uVCOdCZRTrM; douban-fav-remind=1; __utmz=30149280.1603808051.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __gads=ID=7ca757265e2366c5-22ded2176ac40059:T=1603808052:RT=1603808052:S=ALNI_MYZsGZJ8XXb1oU4zxzpMzGdK61LFA; dbcl2="165593539:LvLaPIrgug0"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.16559; ll="118288"; __yadk_uid=DnUc7ftXIqYlQ8RY6pYmLuNPqYp5SFzc; _vwo_uuid_v2=D7ED984782737D7813CC0049180E68C43|1b36a9232bbbe34ac958167d5bdb9a27; ct=y; ck=ZbYm; __utmc=30149280; __utmc=223695111; __utma=30149280.1867171825.1603588354.1613363321.1613372112.11; __utmt=1; __utmb=30149280.2.10.1613372112; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1613372123%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fmovie.douban.com%252Fsubject%252F34841067%252F%253Ffrom%253Dplaying_poster%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.788421403.1612839506.1613363340.1613372123.9; __utmb=223695111.0.10.1613372123; __utmz=223695111.1613372123.9.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; _pk_id.100001.4cf6=e2e8bde436a03ad7.1612839506.9.1613372127.1613363387.',
        }

###评分
def getmovierate():

        url="https://movie.douban.com/cinema/nowplaying/zhanjiang/"
        r = requests.get(url,headers=headers)
        r.encoding = 'utf8'
        s = (r.content)
        selector = etree.HTML(s)
        li_list = selector.xpath('//*[@id="nowplaying"]/div[2]/ul/li')

        dict = {}
        for item in li_list:
            name = item.xpath('.//*[@class="stitle"]/a/@title')[0].replace(" ","").replace("\n","")
            rate = item.xpath('.//*[@class="subject-rate"]/text()')[0].replace(" ", "").replace("\n", "")
            dict[name] = float(rate)
            print("电影="+name)
            print("评分="+rate)
            print("-------")
        ###从小到大排序
        dict = sorted(dict.items(), key=lambda kv: (kv[1], kv[0]))
        print(dict)
        itemNames = []
        datas = []
        for i in range(len(dict) - 1, -1, -1):
            itemNames.append(dict[i][0])
            datas.append(dict[i][1])

        ###画图
        font_size = 10  # 字体大小
        fig_size = (13, 10)  # 图表大小


        data = ([datas])

        # 更新字体大小
        mpl.rcParams['font.size'] = font_size
        # 更新图表大小
        mpl.rcParams['figure.figsize'] = fig_size
        # 设置柱形图宽度
        bar_width = 0.35

        index = np.arange(len(data[0]))
        # 绘制评分
        rects1 = plt.bar(index, data[0], bar_width, color='#0072BC')

        # X轴标题
        plt.xticks(index + bar_width, itemNames)
        # Y轴范围
        plt.ylim(ymax=10, ymin=0)
        # 图表标题
        plt.title(u'豆瓣评分')
        # 图例显示在图表下方
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)

        # 添加数据标签
        def add_labels(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
                # 柱形图边缘用白色填充，纯粹为了美观
                rect.set_edgecolor('white')

        add_labels(rects1)

        # 图表输出到本地
        plt.savefig('豆瓣评分.png')

###时长
def getmovietime():
    url = "https://movie.douban.com/cinema/nowplaying/zhanjiang/"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf8'
    s = (r.content)
    selector = etree.HTML(s)
    li_list = selector.xpath('//*[@id="nowplaying"]/div[2]/ul/li')

    itemNames = []
    datas = []
    dict = {}
    for item in li_list:
        title = item.xpath('.//*[@class="stitle"]/a/@title')[0].replace(" ", "").replace("\n", "")
        href = item.xpath('.//*[@class="stitle"]/a/@href')[0].replace(" ", "").replace("\n", "")
        itemNames.append(title)
        r = requests.get(href, headers=headers)
        r.encoding = 'utf8'
        s = (r.content)
        selector = etree.HTML(s)
        times = selector.xpath('//*[@property="v:runtime"]/text()')
        type = selector.xpath('//*[@property="v:genre"]/text()')

        datas.append(int(times[0].replace("分钟","")))

        print(title)
        print(times)
        print(type)
        for j in type:
            key = str(j)
            try:
                dict[key] = dict[key] + 1
            except:
                dict[key] = 1
        print("-------")


    #####1.时长可视化
    '''
    itemNames.reverse()
    datas.reverse()

    # 绘图。
    fig, ax = plt.subplots()
    b = ax.barh(range(len(itemNames)), datas, color='#6699CC')

    # 为横向水平的柱图右侧添加数据标签。
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' %
                int(w), ha='left', va='center')

    # 设置Y轴纵坐标上的刻度线标签。
    ax.set_yticks(range(len(itemNames)))
    ax.set_yticklabels(itemNames)
    plt.title('电影时长（分钟）', loc='center', fontsize='15',
              fontweight='bold', color='red')

    #plt.show()
    plt.savefig("电影时长（分钟）")
    '''

    #####2.类型可视化
    ###从小到大排序
    dict = sorted(dict.items(), key=lambda kv: (kv[1], kv[0]))
    print(dict)

    itemNames = []
    datas = []
    for i in range(len(dict) - 1, -1, -1):
        itemNames.append(dict[i][0])
        datas.append(dict[i][1])

    x = range(len(itemNames))
    plt.plot(x, datas, marker='o', mec='r', mfc='w', label=u'电影类型')
    plt.legend()  # 让图例生效
    plt.xticks(x, itemNames, rotation=45)
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"类型")  # X轴标签
    plt.ylabel("数量")  # Y轴标签
    plt.title("电影类型统计")  # 标题
    plt.savefig("电影类型统计.png")

###评论数据
def getmoviecomment():
    url = "https://movie.douban.com/cinema/nowplaying/zhanjiang/"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf8'
    s = (r.content)
    selector = etree.HTML(s)
    li_list = selector.xpath('//*[@id="nowplaying"]/div[2]/ul/li')

    for item in li_list:
        title = item.xpath('.//*[@class="stitle"]/a/@title')[0].replace(" ", "").replace("\n", "")
        href = item.xpath('.//*[@class="stitle"]/a/@href')[0].replace(" ", "").replace("\n", "").replace("/?from=playing_poster", "")
        print("电影=" + title)
        print("链接=" + href)
        ###
        with open(title+".txt","a+",encoding='utf-8') as f:
            for k in range(0,200,20):
                url = href+"/comments?start="+str(k)+"&limit=20&status=P&sort=new_score"
                r = requests.get(url, headers=headers)
                r.encoding = 'utf8'
                s = (r.content)
                selector = etree.HTML(s)
                li_list = selector.xpath('//*[@class="comment-item "]')
                for items in  li_list:

                    text = items.xpath('.//*[@class="short"]/text()')[0]
                    f.write(str(text)+"\n")

        print("-------")
        time.sleep(4)

####词云代码
def jieba_cloud(file_name, icon):
    with open(file_name, 'r', encoding='utf8') as f:
        text = f.read()
        text = text.replace('\n',"").replace("\u3000","").replace("，","").replace("。","")
        word_list = jieba.cut(text)
        result = " ".join(word_list)  # 分词用 隔开
        # 制作中文云词
        icon_name = ""
        if icon == 1:
            icon_name = 'fas fa-hippo'
        elif icon == 2:
            icon_name = 'fas fa-dragon'
        elif icon == 3:
            icon_name = 'fas fa-dog'
        elif icon == 4:
            icon_name = 'fas fa-cat'
        elif icon == 5:
            icon_name = 'fas fa-dove'
        elif icon == 6:
            icon_name = 'fab fa-qq'
        elif icon == 7:
            icon_name = 'fas fa-spider'

        """
        # icon_name='',#国旗
        # icon_name='fas fa-dragon',#翼龙
        icon_name='fas fa-dog',#狗
        # icon_name='fas fa-cat',#猫
        # icon_name='fas fa-dove',#鸽子
        # icon_name='fab fa-qq',#qq
        """
        picp = file_name.split('.')[0] + '.png'
        print(icon_name)
        #if icon_name is not None and len(icon_name) > 0:
        gen_stylecloud(text=result, icon_name=icon_name, font_path='simsun.ttc', output_name=picp)  # 必须加中文字体，否则格式错误
        #else:
        #    gen_stylecloud(text=result, font_path='simsun.ttc', output_name=picp)  # 必须加中文字体，否则格式错误

    return picp

###评论数据词云
def commentanalysis():
    lists = ['刺杀小说家','你好，李焕英','人潮汹涌','侍神令','唐人街探案3','新神榜：哪吒重生','熊出没·狂野大陆']
    for i in range(0,len(lists)):
       title =lists[i]+".txt"
       jieba_cloud(title , int(i+1))

###评分数据
#getmovierate()
###时长和电影类型数据
#getmovietime()
###评论数据
#getmoviecomment()
###评论数据词云
commentanalysis()


