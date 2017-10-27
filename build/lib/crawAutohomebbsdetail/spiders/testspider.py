# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class TestspiderSpider(scrapy.Spider):
    name = 'testspider'
    allowed_domains = ['club.autohome.com.cn']
    start_urls = ['http://club.autohome.com.cn/bbs/thread-c-4069-65076307-1.html']
    # start_urls = ['http://club.autohome.com.cn/bbs/thread-c-4069-66196239-2.html']


    def start_requests(self):

        for url in self.start_urls:
            request = Request(url=url, callback=self.parse)
            request.meta['isjs'] = 'True'
            yield request

    def parse(self, response):
        tcontent = response.meta['tcontent']
        print('text===',tcontent)
