# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from _md5 import md5

import happybase
import pymongo
from datetime import datetime
# from twisted.enterprise import adbapi

# import importlib,sys
from scrapy.conf import settings
from crawAutohomebbsdetail.items import AutohomeBbsSpiderItem

import datetime
import random
#sys.setdefaultencoding('utf-8')

class randomRowKey(object):
    # 生产唯一key
    def getRowKey(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum
class HBaseBBSPipeline(object):
    def __init__(self):
        host = settings['HBASE_HOST']
        self.port = settings['HBASE_PORT']
        self.table_name = settings['HBASE_TABLE']
        # port = settings['HBASE_PORT']
        self.connection = happybase.Connection(host=host,port=self.port,timeout=None, autoconnect=False)
        # self.connection = happybase.Connection(host=host,port=self.port,timeout=None, protocol='compact')
        # self.table = self.connection.table(table_name)

        # print('host=%s'%host)
        # print('port=%s' % self.port)
        # print('table=%s'%self.table_name)



    def process_item(self, item, spider):
        # cl = dict(item)
        randomrkey = randomRowKey()
        rowkey = randomrkey.getRowKey()
        self.connection.open()
        table = self.connection.table(self.table_name)
        # b= self.table.batch()
        if isinstance(item, AutohomeBbsSpiderItem):
            # self.table.put('text', cl)
            print('进入pipline')
            title = item['title']
            titleURL = item['titleURL']
            content = item['content']
            pub_time = item['pub_time']
            author = item['author']
            author_url = item['author_url']
            reg_time = item['reg_time']
            addr = item['addr']
            attent_vehicle = item['attent_vehicle']
            jinghuatie = item['jinghuatie']
            fatieliang = item['fatieliang']
            huitieliang = item['huitieliang']
            # cdate = item['cdate']
            from_url = item['from_url']
            floor = item['floor']
            crawldate = item['crawldate']
            luntanname = item['luntanname']
            print('authorType=',type(author))
            print('authorvalue=',author)
            table.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
            # b.put(md5(str(rowkey).encode('utf-8')).hexdigest(), {
                                     'cf1:title':title,
                                     'cf1:titleURL': titleURL,
                                     'cf1:content': content,
                                     'cf1:pub_time': pub_time,
                                     'cf1:author': author,
                                     'cf1:author_url': author_url,
                                     'cf1:reg_time': reg_time,
                                     'cf1:addr': addr,
                                     'cf1:attent_vehicle': attent_vehicle,
                                     'cf1:jinghuatie': jinghuatie,
                                     'cf1:fatieliang': fatieliang,
                                     'cf1:huitieliang': huitieliang,
                                     'cf1:from_url': from_url,
                                     'cf1:floor': floor,
                                     'cf1:crawldate':crawldate,
                                     'cf1:luntanname': luntanname
                                     })
            # b.send()
        self.connection.close()
        return item



class MongoDBPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        bbsdetail = dict(item)
        self.post.insert(bbsdetail)
        return item

class AutohomeBbsSpiderPipeline(object):

    words_to_filter_one = ['想买', '准备入手', '准备订车', '折', '什么颜色', '哪个好', '很喜欢', '选哪款', '对比']

    words_to_filter_two = ['还是', '怎么样']

    words_to_filter_three = ['ATSL舒适优惠45800合适吗', '广西科帕奇大家觉得多少优惠合适', '本人四十有余,选什么颜色合适', '1.5T昂科威两驱精英与2.4L两驱全新达智能的选择']

    def process_item(self, item, spider):

        if item['pub_time'] is not None and item['pub_time'] != '':
            pub_time_t = datetime.strptime(item['pub_time'], '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            if (now - pub_time_t).days > 7:
                item['week_diff'] = 2
            else:
                item['week_diff'] = 1
        else:
            item['week_diff'] = 0

        for word in self.words_to_filter_one:
            if word in item['content']:
                print( item['content'])
                item['key_level'] = 1
                item['keyword'] = word

                return item

        for word in self.words_to_filter_two:
            if word in item['content']:
                print( item['content'])
                item['key_level'] = 2
                item['keyword'] = word

                return item

        for word in self.words_to_filter_three:
            if word in item['content']:
                print( item['content'])
                item['key_level'] = 3
                item['keyword'] = word

                return item

class outputTextPipeline(object):
    def __init__(self):
        self.limit = 50
        self.file = open('D:/crawlfiles/yiqib30/b30detail2.txt', 'wb');
        #self.filedetail = open('D:/crawlfiles/yiqib30/b30_detail.txt', 'wb');



    def process_item(self, item, spider):
        vaild = True
        print('输出文件')
        if item is not None:
            if isinstance(item,AutohomeBbsSpiderItem):

                line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (item['title'],
                                                                   item['content'],
                                                                   item['pub_time'],
                                                                   item['author'],
                                                                   item['author_url'],
                                                                   item['reg_time'],
                                                                   item['jinghuatie'],
                                                                   item['fatieliang'],
                                                                   item['huitieliang'],
                                                                   item['addr'],
                                                                   item['attent_vehicle'],
                                                                   item['from_url'],
                                                                   item['floor'])
                return item
        else :
            item

class CrawautohomebbsdetailPipeline(object):
    def process_item(self, item, spider):
        return item
