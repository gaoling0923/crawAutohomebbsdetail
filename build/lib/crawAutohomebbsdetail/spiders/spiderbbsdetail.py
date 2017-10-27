# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy import Spider
from crawAutohomebbsdetail.items import AutohomeBbsSpiderItem

import re
import time

#import sys
#reload(sys)
import sys

#sys.setdefaultencoding('utf-8')
class spiderbbsdetail(Spider):
    name = "spiderbbsdetail"
    allowed_domains = ["club.autohome.com.cn"]
    start_urls = [
        # 别克 GL8 论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-166-1.html',
        # 北京地区论坛
        #'http://club.autohome.com.cn/bbs/forum-a-100002-1.html',
        # 'http://club.autohome.com.cn/bbs/forum-c-3695-1.html',#奔腾B30论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-632-1.html', #奔腾B50论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-466-1.html',#奔腾B70论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-2310-1.html',#奔腾B90论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-4069-1.html',#奔腾X40论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-3000-1.html',#奔腾X80论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-4117-1.html',#奔腾X4论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-4114-1.html',#奔腾X6论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-3579-1.html'#奔腾X70论坛
        'http://club.autohome.com.cn/bbs/forum-c-4166-1.html' #宝骏510论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-3824-1.html' #森雅R7论坛
        # 'http://club.autohome.com.cn/bbs/forum-c-2778-1.html' #长安
        # 'http://club.autohome.com.cn/bbs/forum-c-3080-1.html' #瑞风S3论坛
    ]
    def __init__(self, **kwargs):
        #super();
        self.count=0
        self.titilurl=''
    def start_requests(self):
        # urls = [
        #    'http://k.autohome.com.cn/4069/',
        # ]

        for url in self.start_urls:
            print('>>> 爬取开始>>> ', url)
            self._wait()
            request = Request(url=url, callback=self.parse)
            request.meta['isjs'] = 'False'
            yield request

    def parse(self, response):
        print('>>> 开始爬取论坛下所有的文章列表>>> ',response.url)
        # self._wait()
        self.count = self.count + 1
        # print('当前页数：==', self.count)
        # logger.log(logging.INFO, '当前页数：%s' % self.count)
        # 获取总页数 { DOM: 共xxx页 }
        #//*[@id="subcontent"]/div[1]/div[2]/span[2]/span
        #total_page_text = response.xpath('//div[@class="pagearea"]/span[@class="fr"]/text()').extract()[0]
        total_page_text = response.xpath('//*[@id="subcontent"]/div[1]/div[2]/span[2]/span/text()').extract_first()
        print('total_page==', total_page_text)

        # 截取首尾字符串, 得到总页数
        total_page = total_page_text[2:][:-1]
        # if total_page_text is not None:
        #     total_page = total_page_text[2:][:-1]
        # else:
        #     total_page = 1


        # 当前页面的 URL
        curr_url = response.url

        # replace str to >> -{{page}}.html
        p = re.compile('(-)\d+(.html$)')
        repl_url = re.sub(p, '\\1{{page}}\\2', curr_url)

        # 接下来要爬取的URLs
        next_urls = [repl_url.replace('{{page}}', str(i)) for i in range(2, int(total_page)+1)]

        for next_url in next_urls:
            print('>>> 开始爬取论坛下所有的文章的标题和超链接 %s ' % next_url)
            self._wait()
            # yield Request(next_url, callback=self.parse_paged_list)
            request = Request(next_url, callback=self.parse_paged_list)
            request.meta['isjs'] = 'False'
            yield request
        # # 爬取本页内的
        self.parse_paged_list(response)


    def parse_paged_list(self, response):
        # print('>>> 开始爬取论坛下所有的文章的标题和超链接')
        # self._wait()

        resp_a = response.xpath('//div[@id="subcontent"]/dl[@lang]/dt/a')
        texts = resp_a.xpath('text()').extract()
        hrefs = resp_a.xpath('@href').extract()

        if len(texts) != len(hrefs):
            raise Exception('标题 和 对应的链接不匹配, 请排查文档结构是否有变动')

        for i in range(0, len(texts)):
            # like '/bbs/thread-c-166-5968706-1.html'
            href_sub = hrefs[i]
            hrefs[i] = 'http://club.autohome.com.cn' + href_sub
            # print('>>> ', texts[i].strip(), ' <<< ', hrefs[i])
            # time.sleep(0.3)

        # next_urls = response.xpath('//div[@id="subcontent"]/dl[@lang]/dt/a/@href').extract()
        for next_url in hrefs:
            print('>>> 开始爬取帖子内容 <<<', next_url)
            self._wait()
            request= Request(next_url, callback=self.parse_post_url_pages)
            request.meta['isjs'] = 'True'
            yield request

    def parse_post_url_pages(self, response):
        #>>> 开始爬取帖子内容 <<<

        # print('>>> ', texts[i].strip(), ' <<< ', hrefs[i])
        # self._wait()

        # 总页码 #x-pages2 > span.gopage > span
        #total_page = response.xpath('//div[@class="pagearea"]//span[@class="fs"]/text()').extract()[0][3:][:-2]
        #total_pagetext = response.xpath('//*[@id="x-pages2"]/span[3]/span/text()').extract()
        #print('>>> [post] total_pagetext <<< ', total_pagetext)
        #total_page = total_pagetext[0][3:][:-2]
       # print('>>> [post] Total Page <<< ', total_page)

        # 当前页面的 URL
        curr_url = response.url
        print('curr_url:',curr_url)
        # print('>>> 开始爬取帖子下所有分页的链接地址：',curr_url)


        p = re.compile('(-)\d+(.html$)')
        repl_url = re.sub(p, '\\1{{page}}\\2', curr_url)
        # print('repl_url:', repl_url)
        # 接下来要爬取的URLs
        titilURL=repl_url.replace('{{page}}', str(1));

        # replace str to >> -{{page}}.html
       # p = re.compile('(-)\d+(.html$)')
       # repl_url = re.sub(p, '\\1{{page}}\\2', curr_url)

        # 接下来要爬取的URLs
        #next_urls = [repl_url.replace('{{page}}', str(i)) for i in range(2, int(total_page) + 1)]

        #for next_url in next_urls:
        #    print('>>> [post] ', next_url)
        #    # time.sleep(0.3)
        #    yield Request(next_url, callback=self.parse)

        # print('>>> 开始爬取帖子内容 <<< ', response.url)
        #
        # self._wait();
        # 如果当前爬取的页面是第一页, 则爬取楼主发表的内容
        tcontent = response.meta['tcontent']

        maintopic_dom = response.css('div#cont_main div#maxwrap-maintopic')

        # 论坛文章的标题
        title_arr = maintopic_dom.css('div#consnav span:last-child::text').extract()
        title = title_arr[0] if title_arr else ''
        luntanname1 = maintopic_dom.css('.consnav  span:nth-child(2)  a::text').extract_first();
        if response.url.find('-1.html') == -1:
            print('第一页==',response.url)
        else:
            # 采用 css 选择器的规则
            # 论坛主题内容 DOM 父元素
            # maintopic_dom = response.css('div#cont_main div#maxwrap-maintopic')
            #
            # # 论坛文章的标题
            # title_arr = maintopic_dom.css('div#consnav span:last-child::text').extract()
            # title = title_arr[0] if title_arr else ''
            # 文章内容 DOM 父元素
            contstxt_dom = maintopic_dom.css('div.contstxt')

            # 文章发表时间
            pubtime_arr = contstxt_dom.css('div.conright div.rtopcon span[xname=date]::text').extract()
            pubtime = pubtime_arr[0] if pubtime_arr else ''

            # 论坛文章的内容 (HTML 代码), , 采用 css 选择器的规则
            contents = contstxt_dom.css(
                'div.conright div.rconten div.conttxt div.w740 div.tz-paragraph *::text').extract()

            # 文章作者 和 个人主页
            author_a_dom = maintopic_dom.css('div.conleft ul.maxw li.txtcenter a.c01439a')
            author_arr = author_a_dom.css('::text').extract()
            author = author_arr[0].strip() if author_arr else '空'
            author_url_arr = author_a_dom.css('::attr(href)').extract()
            author_url = author_url_arr[0] if author_url_arr else ''

            # 作者注册时间 #F2 > div.conleft.fl > ul.leftlist > li:nth-child(5)
            reg_time_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(5)::text').extract()
            reg_time = reg_time_arr[0] if reg_time_arr else ''
            reg_time = reg_time[3:] if reg_time else ''

            # jinghuadie
            jinghuatie = maintopic_dom.css('div.conleft.fl  ul.leftlist  li:nth-child(3) a::text').extract_first();
            print('精华帖', jinghuatie)
            if jinghuatie is None:
                print('帖子空')
                jinghuatie = '0'

            # 发帖量
            # F2 > div.conleft.fl > ul.leftlist > li:nth-child(4) > a:nth-child(1)
            fatieliang = maintopic_dom.css(
                'div.conleft ul.leftlist li:nth-child(4)  a:nth-child(1)::text').extract_first();

            # print('发帖量',fatieliang)
            # 回复量 F2 > div.conleft.fl > ul.leftlist > li:nth-child(4) > a:nth-child(3)
            huitieliang = maintopic_dom.css(
                'div.conleft ul.leftlist li:nth-child(4)  a:nth-child(3)::text').extract_first();
            # print('发帖量',huitieliang)
            # 作者所在地
            addr_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(6) a.c01439a::text').extract()
            addr = addr_arr[0] if addr_arr else ''
            # 作者关注车型
            attent_vehicle_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(7) a.c01439a::text').extract()
            attent_vehicle = attent_vehicle_arr[0] if attent_vehicle_arr else ''

            # luntanname1=maintopic_dom.css('.consnav  span:nth-child(2)  a::text').extract_first();

            print('=============================== TiTle Gold Line ================================')
            print('文章标题 ==> ', title)
            print('文章标题URL==》',titilURL)
            # print('发表时间 ==>', pubtime)
            # print('作者 ==> ', author)
            # print('个人主页 ==> ', author_url)
            # print('注册时间 ==> ', reg_time)
            # print('所在地 ==> ', addr)
            # print('关注车型 ==> ', attent_vehicle)
            # # jinghuadie
            # print('精华帖 ==> ', str(jinghuatie).replace('帖', ''))
            # print('发帖量 ==> ', str(fatieliang).replace('帖', ''))
            # print('回帖量 ==> ', str(huitieliang).replace('回', ''))
            # print('文章主题内容 ==>',tcontent)

            # tcontent = ''
            # for c in contents:
            #     if c.strip():
            #         # print(c)
            #         tcontent = tcontent + c.strip()

            topic_item = AutohomeBbsSpiderItem()
            topic_item['title'] = title.strip() if title else ''

            topic_item['titleURL'] = titilURL.strip() if title else ''
            topic_item['content'] = tcontent.strip() if tcontent else ''
            topic_item['pub_time'] = pubtime.strip() if pubtime else ''
            topic_item['author'] = str(author.strip()) if author else ''
            topic_item['author_url'] = author_url.strip() if author_url else ''
            topic_item['reg_time'] = reg_time.strip() if reg_time else ''
            topic_item['addr'] = addr.strip() if addr else ''
            topic_item['attent_vehicle'] = attent_vehicle.strip() if attent_vehicle else ''
            topic_item['from_url'] = response.url
            topic_item['floor'] = '楼主'
            # str(jinghuadie).replace('帖', '')
            topic_item['jinghuatie'] = str(jinghuatie).replace('帖', '')
            topic_item['fatieliang'] = str(fatieliang).replace('帖', '')
            topic_item['huitieliang'] = str(huitieliang).replace('回', '')
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            topic_item['crawldate'] = nowTime
            topic_item['luntanname'] = luntanname1 if luntanname1 else ''
            # topic_item['luntanname'] ='benteng'

            yield topic_item

        ## 论坛文章回复的内容 ##
        reply_doms = response.css('div#cont_main div#maxwrap-reply div.contstxt')

        for reply_dom in reply_doms:


            reply_author_a_dom = reply_dom.css('div.conleft ul.maxw li.txtcenter a.c01439a')
            reply_pub_time = reply_dom.css('div.conright div.rtopconnext span[xname=date]::text').extract()[0]

            reply_author = reply_author_a_dom.css('::text').extract()[0]

            reply_author_url = reply_author_a_dom.css('::attr(href)').extract()[0]

            reply_floor = \
            reply_dom.css('div.conright div.rconten div.rtopconnext div.fr button.rightbutlz::text').extract()[0]

            # 作者注册时间
            reply_reg_time = reply_dom.css('div.conleft ul.leftlist li:nth-child(5)::text').extract()[0]
            reply_reg_time = reply_reg_time[3:] if reply_reg_time else ''

            # 作者所在地
            reply_addr = reply_dom.css('div.conleft ul.leftlist li:nth-child(6) a.c01439a::text').extract()[0]

            # 作者关注车型
            reply_attent_vehicle_arr = reply_dom.css(
                'div.conleft ul.leftlist li:nth-child(7) a.c01439a::text').extract()
            reply_attent_vehicle = reply_attent_vehicle_arr[0] if reply_attent_vehicle_arr else ''

            # 精华帖
            rjinghuatie = reply_dom.css('div.conleft.fl  ul.leftlist  li:nth-child(3)  a::text').extract_first();
            # print('精华帖', rjinghuatie)
            if rjinghuatie is None:
                rjinghuatie = '0'
            # 发帖量
            # F2 > div.conleft.fl > ul.leftlist > li:nth-child(4) > a:nth-child(1)
            fatieliang = reply_dom.css(
                'div.conleft ul.leftlist li:nth-child(4)  a:nth-child(1)::text').extract_first();
            # print('发帖量',fatieliang)
            # 回复量 F2 > div.conleft.fl > ul.leftlist > li:nth-child(4) > a:nth-child(3)
            huitieliang = reply_dom.css(
                'div.conleft ul.leftlist li:nth-child(4)  a:nth-child(3)::text').extract_first();
            # print('发帖量',huitieliang)

            reply_contents_dom = reply_dom.css('div.conright div.rconten div.x-reply div.w740')
            reply_contents = []
            if (reply_contents_dom.css('div.yy_reply_cont')):
                reply_contents = reply_contents_dom.css('div.yy_reply_cont *::text').extract()
            else:
                reply_contents = reply_contents_dom.css('*::text').extract()

            luntanname2 = reply_doms.css('consnav span:nth-child(2)  a::text').extract_first();

            # print('论坛 ==> ', luntanname1)
            # print('回复人 ==> ', reply_author)
            # print('发表时间 ==>', reply_pub_time)
            # print('回复人主页 ==> ', reply_author_url)
            # print('回复人注册时间 ==> ', reply_reg_time)
            # print('回复人所在地 ==> ', reply_addr)
            # print('回复人关注车型 ==> ', reply_attent_vehicle)
            # print('精华帖 ==>', rjinghuatie)
            # print('楼层 ==>', reply_floor)
            # print('回复内容 ==>')

            reply_content = ''
            for c in reply_contents:
                if c.strip():
                    # print(c)
                    reply_content = reply_content + c

            reply_item = AutohomeBbsSpiderItem()
            reply_item['title'] = title.strip() if title else ''
            reply_item['titleURL'] = titilURL.strip() if titilURL else ''
            reply_item['content'] = reply_content.strip() if reply_content else ''
            reply_item['pub_time'] = reply_pub_time.strip() if reply_pub_time else ''
            reply_item['author'] = reply_author.strip() if reply_author else ''
            reply_item['author_url'] = reply_author_url.strip() if reply_author_url else ''
            reply_item['reg_time'] = reply_reg_time.strip() if reply_reg_time else ''
            reply_item['addr'] = reply_addr.strip() if reply_addr else ''
            reply_item['attent_vehicle'] = reply_attent_vehicle.strip() if reply_attent_vehicle else ''
            reply_item['from_url'] = response.url
            reply_item['floor'] = reply_floor.strip() if reply_floor else ''
            reply_item['jinghuatie'] = rjinghuatie.strip() if rjinghuatie else ''
            reply_item['fatieliang'] = str(fatieliang).replace('帖', '')
            reply_item['huitieliang'] = str(huitieliang).replace('回', '')

            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            reply_item['crawldate'] = nowTime
            reply_item['luntanname'] = luntanname1 if luntanname1 else ''
            # reply_item['luntanname'] ='benteng'

            yield reply_item

        self._wait()
        next = response.css('.pagearea .pages .afpage::attr(href)').extract_first();
        nurl=response.urljoin(next);
        yield Request(nurl, callback=self.parse_post_url_pages)


    def _wait(self):
        for i in range(0, 3):
            print('.' * (i%3+1))
            time.sleep(1)


