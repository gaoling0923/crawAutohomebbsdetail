# -*- coding: utf-8 -*-

# Scrapy settings for crawAutohomebbsdetail project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawAutohomebbsdetail'

SPIDER_MODULES = ['crawAutohomebbsdetail.spiders']
NEWSPIDER_MODULE = 'crawAutohomebbsdetail.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawAutohomebbsdetail (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# LOG_FILE = 'D:/crawlogs/crawlAutohomeBBSDetail.log'
# LOG_LEVEL = 'DEBUG'
# LOG_STDOUT=True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS =32

DOWNLOAD_TIMEOUT=60
# RETRY_ENABLED = False

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED =False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawAutohomebbsdetail.middlewares.CrawautohomebbsdetailSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawAutohomebbsdetail.middlewares.MyCustomDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'crawAutohomebbsdetail.middlewares.MyCustomDownloaderMiddleware': None,
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 200,
    # 'crawAutohomebbsdetail.middlewares.proxMiddleware': 300,
    'crawAutohomebbsdetail.middlewares.JavaScriptMiddleware': 543
    # 'crawAutohomebbsdetail.middlewares.proxMiddleware':None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'crawAutohomebbsdetail.pipelines.CrawautohomebbsdetailPipeline': 300,
#}
ITEM_PIPELINES = {
    # 'autohome_bbs_spider.pipelines.AutohomeBbsSpiderPipeline': 1,
    #'crawAutohomebbsdetail.pipelines.proxMiddleware': 1,
    # 'crawAutohomebbsdetail.pipelines.AutohomeBbsSpiderPipeline': None,
    # 'crawAutohomebbsdetail.pipelines.outputTextPipeline': None,
    # 'crawAutohomebbsdetail.pipelines.MongoDBPipeline':300
    'crawAutohomebbsdetail.pipelines.HBaseBBSPipeline':300

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#连接数据库的信息，存到mydb的articles数据集中
MONGODB_HOST="localhost"
MONGODB_PORT=27017
MONGODB_DBNAME="autohome"
MONGODB_DOCNAME="bbsdetail2"


HBASE_HOST = '10.8.23.6'
# HBASE_HOST = '192.168.0.95'
HBASE_PORT = 9090
# HBASE_TABLE = 'testdb'
HBASE_TABLE = 'autoHomeBBSTitleDetail'

PROXY_POOL_URL = 'http://localhost:5000/get'

