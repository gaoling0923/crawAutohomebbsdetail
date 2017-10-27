# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
import time

from scrapy import signals
from scrapy.conf import settings
import random
# from crawAutohomebbsdetail.dbpackage.dbresdis import RedisClient
from selenium.webdriver.common.proxy import ProxyType

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class proxMiddleware(object):
    proxy_list=[
        "http://119.28.136.72:3128",
     "http://176.104.196.234:8081"
     "http://176.104.196.234:8081"
     "http://176.104.196.234:8081"
     "http://176.104.196.234:8081"
     "http://200.48.129.123:8080"]

    def process_request(self, request, spider):
        # if not request.meta['proxies']:
        # ip = random.choice(self.proxy_list)
        ip = self.get_proxy()
        print('process IP:',ip)
        # print 'ip=' %ip
        request.meta['proxy'] = ip
    def get_proxy(self):
        try:
            response = requests.get(settings['PROXY_POOL_URL'])
            if response.status_code == 200:

                return response.text
            return None
        except ConnectionError:
            return None

class JavaScriptProxyMiddleware(object):

    def process_request(self, request, spider):
        # conn = RedisClient();
        # proxy = conn.pop();
        # print('当前使用的IP:', proxy);
        # request.meta['proxy'] = "http://%s" % proxy

        # proxy=self.get_proxy()
        if spider.name in("spiderbbsdetail","crawlb30bbsdetail"):
            print("execute PhantomJS spiderName", spider.name);
            print("PhantomJS is starting..")
            driver = webdriver.PhantomJS() #指定使用的浏览器
            #driver =webdriver.Chrome()
            # driver = webdriver.Firefox()
            # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxyip=self.get_proxy()
            print('PROXY_IP:', proxyip)

            if proxyip:
                print('进入:', proxyip)
                proxy.http_proxy = proxyip

                # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.get(request.url)
                # print('1: ', driver.session_id)
                # print('2: ', driver.page_source)
                # print('3: ', driver.get_cookies())
                # js = "var q=document.documentElement.scrollTop=10000"
                # browser.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
                # time.sleep(3)
                body = driver.page_source
                # print ("访问2="+body)
                print ("访问="+request.url)
                return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            else:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.DIRECT
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
                driver.get(request.url)
                body = driver.page_source
                return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

        else:
            return

    def get_proxy(self):
        try:
            response = requests.get(settings['PROXY_POOL_URL'])
            if response.status_code == 200:

                return response.text
            return None
        except ConnectionError:
            return None
class JavaScriptMiddleware(object):

    # def __init__(self):
    #     browser = webdriver.PhantomJS()

    def process_request(self, request, spider):
        # conn = RedisClient();
        # proxy = conn.pop();
        # print('当前使用的IP:', proxy);
        # request.meta['proxy'] = "http://%s" % proxy
        # if spider.name in("spiderbbsdetail","crawlb30bbsdetail"):
        print("execute PhantomJS spiderName", spider.name);
        print("PhantomJS is starting..")
        browser = webdriver.PhantomJS() #指定使用的浏览器
        # browser =webdriver.Chrome()
        # driver = webdriver.Firefox()
        # time.sleep(1)
        # driver.implicitly_wait(30)  # seconds
        # wait = WebDriverWait(driver, 60)
        browser.get(request.url)
        print("访问=" + request.url)
        body = browser.page_source
        # 等待完成

        # proxy = webdriver.Proxy()
        # proxy.proxy_type = ProxyType.MANUAL
        # proxyip = self.get_proxy()
        # print('PROXY_IP:', proxyip)
        # # response = ''
        # if proxyip:
        #     print('进入:', proxyip)
        #     proxy.http_proxy = proxyip
        #
        #     # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
        #     proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        #     browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        #     browser.get(request.url)
        #     # print('1: ', driver.session_id)
        #     # print('2: ', driver.page_source)
        #     # print('3: ', driver.get_cookies())
        #     # js = "var q=document.documentElement.scrollTop=10000"
        #     # browser.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
        #     # time.sleep(3)
        #     body = browser.page_source
        #     # print ("访问2="+body)
        #     print("访问=" + request.url)
        #     response = HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
        # else:
        #     proxy = webdriver.Proxy()
        #     proxy.proxy_type = ProxyType.DIRECT
        #     proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        #     browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        #     browser.get(request.url)
        #     body = browser.page_source
        #     response = HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)


        response= HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
        # response= HtmlResponse(browser.current_url, body=body, encoding='gbk', request=request)
        # response= HtmlResponse(browser.current_url, body=body,  request=request)
        soup = BeautifulSoup(response.text, 'lxml')

        # request.meta.
        isjs= request.meta['isjs']

        content=''
        koubei_content = ''
        print('isjs=%s'% isjs)
        if isjs == 'True':
            # print(body)
            ##有可能多个内容
            print('进入。。。。')

            # print('maintopic',maintopic)

            maintopic = soup.find(id='maxwrap-maintopic')
            mouthcons = maintopic.findAll('div', class_='conttxt')
            # print('mouthcons=%s' % mouthcons)
            # koubei_content = mouthcons[0]
            for mouthcon in mouthcons:
                # type = mouthcon.find('i', class_='icon icon-zj').get_text()
                # if type == '口碑':
                # print()
                koubei_content = mouthcon
                    # 正文内容
            if koubei_content:
                text_con = koubei_content.find('div', class_='tz-paragraph')
                # print('text_con=%s'%text_con)
                if text_con:
                    replace_content_s_list = text_con.findAll('span')
                    if replace_content_s_list :
                        print('replace_content_s_list==',replace_content_s_list)
                        # 等待完成
                        first_class = replace_content_s_list[0].attrs['class'][0]
                        # print('first_class==',first_class)
                        element_present = EC.presence_of_element_located((By.CLASS_NAME, first_class))
                        WebDriverWait(browser, 60).until(element_present)

                        # 字典，存储获取过的内容
                        span_class_dict = {}
                        for replace_span_s in replace_content_s_list:
                            cls = replace_span_s.attrs['class'][0]
                            if cls not in span_class_dict:
                                script = "return window.getComputedStyle(document.getElementsByClassName('%s')[0],'before').getPropertyValue('content')" % (
                                    cls)
                                trans = browser.execute_script(script).strip('\"')
                                span_class_dict[cls] = trans
                            replace_span_s.replace_with(span_class_dict[cls])

                        # print(body)
                        # 清除style和script
                        [i.extract() for i in koubei_content.findAll('style')]
                        [i.extract() for i in koubei_content.findAll('script')]

                        content = koubei_content.get_text(strip=True)

                    else:
                        content=text_con.get_text(strip=True)



        # print('content=',content)
        request.meta['tcontent']=content

        browser.close()
        # time.sleep(3)
        # browser.implicitly_wait(30)  # seconds
        # return HtmlResponse(browser.current_url, body=body, encoding='utf-8', request=request)
        return response
    def get_proxy(self):
        try:
            response = requests.get(settings['PROXY_POOL_URL'])
            if response.status_code == 200:

                return response.text
            return None
        except ConnectionError:
            return None
class CrawautohomebbsdetailSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
