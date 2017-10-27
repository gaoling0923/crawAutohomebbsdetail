# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawautohomebbsdetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class AutohomeBbsSpiderItem(scrapy.Item):

    title = scrapy.Field()#标题
    titleURL = scrapy.Field()  # 标题
    content = scrapy.Field()#内容
    pub_time = scrapy.Field()#发布时间

    author = scrapy.Field()#作者
    author_url = scrapy.Field()#作者url
    reg_time = scrapy.Field()#注册时间
    addr = scrapy.Field()#来自
    attent_vehicle = scrapy.Field()#关注车型
    jinghuatie = scrapy.Field()  # 精华帖
    fatieliang = scrapy.Field()  # 发帖量
    huitieliang = scrapy.Field()  # 回帖

    cdate = scrapy.Field()
    from_url = scrapy.Field()#url

    floor = scrapy.Field() #楼层
    crawldate = scrapy.Field()
    luntanname = scrapy.Field() #论坛名称
