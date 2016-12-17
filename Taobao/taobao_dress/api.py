# coding=utf-8
# usr/bin/eny python

import requests
import re
import json
import time
import urllib.request
import pymysql.cursors

class Taobao(object):

    def __init__(self,theme):
        self.theme = urllib.request.quote(theme)   # 连衣裙类型
        self.conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root',
                               passwd = '',db = 'taobao_db',charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.info_sql = "INSERT IGNORE INTO `address` VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"


    def sovl_dict(self,contents):
        '''
        解析字典
        '''
        for content in contents:
            if 'itemId' in content:
                goods_id = content['itemId']
            elif 'nid' in content:
                goods_id = content['nid']
            else:
                goods_id = u" "

            if 'sellerId' in content:
                shop_id = content['sellerId']
            elif 'user_id' in content:
                shop_id = content['user_id']
            else:
                shop_id = u" "

            if 'item_loc' in content:
                shop_loc = content['item_loc']
            else:
                shop_loc = u" "

            if 'nick' in content:
                shop_name = content['nick']
            else:
                shop_name = u" "

            if 'title' in content:
                goods_title = content['title']
            elif 'raw_title' in content:
                goods_title = content['raw_title']
            else:
                goods_title = u" "

            if 'recommendReason' in content:
                view_sales = content['recommendReason']
            elif 'view_sales' in content:
                view_sales = content['view_sales']
            else:
                view_sales = u" "

            if 'salePrice' in content:
                view_price = content['salePrice']
            elif 'view_price' in content:
                view_price = content['view_price']
            else:
                view_price = u" "

            if 'url' in content:
                comment_url = content['url']
            elif 'comment_url' in content:
                comment_url = content['comment_url']
            else:
                comment_url = u" "
            comment_url = 'https:' + comment_url

            print("{0}::{1}::{2}::{3}::{4}::{5}".format(goods_id, shop_id, goods_title, \
                                                        view_sales, view_price, comment_url))
            self.cursor.execute(self.info_sql, (str(goods_id), str(shop_id), shop_loc, shop_name, goods_title, \
                                                str(view_sales), str(view_price), comment_url))
            self.conn.commit()
            return goods_id,shop_id


    def first_content(self,first_url):
        '''
        首页商品信息页
        '''
        s = requests.get(first_url)
        contents = s.content.decode('utf-8')
        regex = 'g_page_config = (.+)'
        items = re.findall(regex, contents)
        items = items.pop().strip()
        items = items[0:-1]
        items = json.loads(items)
        items = items['mods']['itemlist']['data']['auctions']
        if items == []:
            return
        else:
            goods_id,shop_id = self.sovl_dict(items)
            self.second_content(goods_id, shop_id)   # 爬取二级页面
            # time.sleep(1)


    def second_content(self,goods_id,shop_id):
        '''
        二级页面的商品信息
        '''
        print('——*———— 二级页面 ————*—— ')
        second_url = 'https://tui.taobao.com/recommend?itemid={0}&sellerid={1}&_ksTS=&callback=jsonp&appid=3066'\
                                                                                        .format(goods_id,shop_id)
        s = requests.get(second_url)
        contents = s.content.decode('gbk')
        regex = 'jsonp(.+)'
        items = re.findall(regex, contents)
        items = items.pop()
        items = items[1:-2]
        items = json.loads(items)
        items = items['result']
        if items == []:
            return
        else:
            self.sovl_dict(items)


    def run(self):
        '''
        运行
        '''
        try:
            for i in range(100):
                first_url = 'https://s.taobao.com/search?spm=&q={0}&bcoffset=&ntoffset&p4ppushleft=1%2C48&s={1}'\
                                                                                    .format(self.theme, (i+1)*44)
                self.first_content(first_url)
        except Exception as e:
            print(e)
