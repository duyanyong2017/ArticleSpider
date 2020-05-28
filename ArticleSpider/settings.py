# -*- coding: utf-8 -*-

# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16


# 当COOKIES_ENABLED是注释的时候scrapy默认没有开启cookie
# 当COOKIES_ENABLED没有注释设置为False的时候scrapy默认使用了settings里面的cookie
# 当COOKIES_ENABLED设置为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie
# 所以当我使用settings的cookie的时候，又把COOKIES_ENABLED设置为True，scrapy就会把settings的cookie关闭，
# 而且我也没使用自定义cookie，导致整个请求根本没有cookie,导致获取页面失败。
# 总结：
# 如果使用自定义cookie就把COOKIES_ENABLED设置为True
# Disable cookies (enabled by default)
COOKIES_ENABLED = False # 设置为True 或者 注释掉都会被反爬，原因不详

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'ArticleSpider.middlewares.RandomUserAgentMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    'ArticleSpider.pipelines.ImagesPipeline': 1,
    'ArticleSpider.pipelines.JsonWithEncodingPipeline': 2,
    # 'ArticleSpider.pipelines.MysqlPipeline': 2,
    'ArticleSpider.pipelines.MysqlTwistedPipeline': 3,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


import os

IMAGES_URLS_FIELD = 'front_image_url'
project_dir = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')

import sys

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'ArticleSpider'))

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'imooc'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'dyy@123'

# from datetime import datetime
#
# TODAY = datetime.now().strftime("%Y%m%d")
# LOG_ENABLED = 'True'
# LOG_ENCODING = 'utf-8'
# import platform
#
# LOG_FILE = '\\'.join((BASE_DIR, 'ArticleSpider', 'log', TODAY)) if platform.system() == 'Windows' else '//'.join(
#     (BASE_DIR, 'ArticleSpider', 'log', TODAY))
# LOG_LEVEL = 'DEBUG'
# REDIRECT_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "referer": "https://www.lagou.com",
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/json;charset=utf-8'}
