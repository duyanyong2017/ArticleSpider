# -*- coding: utf-8 -*-
import os
import pickle
import time
from datetime import datetime
import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import LagouJobItemLoader, LagouJobItem
from settings import BASE_DIR  # , LOG_FILE
from utils.common import get_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']
    headers = {
        "HOST": "www.lagou.com"
    }
    # custom_settings = {
    #     "COOKIES_ENABLED": False,
    #     "DOWNLOAD_DELAY": 1,
    #     'DEFAULT_REQUEST_HEADERS': {
    #         'Accept': 'application/json, text/javascript, */*; q=0.01',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.8',
    #         'Connection': 'keep-alive',
    #         # 'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBC99154D1A744BD8AD12BA0DEE80F320; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _ga=GA1.2.1111395267.1516570248; _gid=GA1.2.1409769975.1516570248; user_trace_token=20180122053048-58e2991f-fef2-11e7-b2dc-525400f775ce; PRE_UTM=; LGUID=20180122053048-58e29cd9-fef2-11e7-b2dc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=7e9c503b9a29e06e6d130f153c562827; _gat=1; LGSID=20180122055709-0762fae6-fef6-11e7-b2e0-525400f775ce; PRE_HOST=github.com; PRE_SITE=https%3A%2F%2Fgithub.com%2Fconghuaicai%2Fscrapy-spider-templetes; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4060662.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516569758,1516570249,1516570359,1516571830; _putrc=88264D20130653A0; login=true; unick=%E7%94%B0%E5%B2%A9; gate_login_token=3426bce7c3aa91eec701c73101f84e2c7ca7b33483e39ba5; LGRID=20180122060053-8c9fb52e-fef6-11e7-a59f-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516572053; TG-TRACK-CODE=index_navigation; SEARCH_ID=a39c9c98259643d085e917c740303cc7',
    #         'Host': 'www.lagou.com',
    #         'Origin': 'https://www.lagou.com',
    #         'Referer': 'https://www.lagou.com/',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    #     }
    # }

    # start_urls = ['https://www.lagou.com/jobs/list_/p-city_6']
    # start_urls = ['https://www.lagou.com/jobs/6981517.html?show=31517064ea2541b2b11f29661698f07d']

    rules = (
        # 全站爬取
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def start_requests(self):
        #     from selenium import webdriver
        #     options = webdriver.ChromeOptions()
        #     options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        #     browser = webdriver.Chrome(
        #         executable_path=r"D:\softwares\chromedriver.exe"
        #         , options=options
        #     )
        #
        #     browser.get("https://sec.lagou.com/verify.html?e=3&f=https://www.lagou.com/jobs/3182310.html")
        #     browser.find_element_by_xpath('//div[@class="container"]/a[@id="btn"]').click()

        cookies = []
        if os.path.exists(BASE_DIR + "\cookies\lagou.cookie") and os.path.getsize(
                BASE_DIR + "\cookies\lagou.cookie") > 0:
            cookies = pickle.load(open(BASE_DIR + "\cookies\lagou.cookie", "rb"))

        if not cookies:
            from selenium import webdriver
            options = webdriver.ChromeOptions()
            options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            browser = webdriver.Chrome(
                executable_path=r"D:\softwares\chromedriver.exe"
                , options=options
            )
            browser.get("https://passport.lagou.com/login/login.html")
            browser.find_element_by_css_selector(".form_body .input.input_white").send_keys("18896738910")
            browser.find_element_by_css_selector(".form_body input[type='password']").send_keys("duyanyong@320324")
            browser.find_element_by_css_selector("div[data-view='passwordLogin'] input.btn_lg").click()

            time.sleep(5)
            cookies = browser.get_cookies()

            pickle.dump(cookies, open(BASE_DIR + "\cookies\lagou.cookie", "wb"))

        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict)

    def parse_job(self, response):
        # logger = logging.getLogger()
        # formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        #
        # file_hadler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
        # file_hadler.setLevel(level=logging.DEBUG)
        # file_hadler.setFormatter(formatter)
        #
        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.DEBUG)
        # stream_handler.setFormatter(formatter)
        #
        # logger.addHandler(file_hadler)
        # logger.addHandler(stream_handler)
        #
        # logger.info(response.url)

        itemloader = LagouJobItemLoader(item=LagouJobItem(), response=response)

        itemloader.add_css("title", ".job-name::attr(title)")
        itemloader.add_value("url", response.url)
        itemloader.add_value('url_object_id', get_md5(response.url))
        itemloader.add_css("salary", ".job_request .salary::text")
        itemloader.add_xpath("job_city", "//*[@class='job_request']/h3/span[2]/text()")
        itemloader.add_xpath("work_years", "//*[@class='job_request']/h3/span[3]/text()")
        itemloader.add_xpath("degree_need", "//*[@class='job_request']/h3/span[4]/text()")
        itemloader.add_xpath("job_type", "//*[@class='job_request']/h3/span[5]/text()")

        itemloader.add_css("tags", '.position-label li::text')
        itemloader.add_css('publish_time', '.publish_time::text')
        itemloader.add_css('job_advantage', '.job-advantage p::text')
        itemloader.add_css('job_desc', '.job_bt div')
        itemloader.add_css('job_addr', '.work_addr')
        itemloader.add_css('company_name', '#job_company dt a img::attr(alt)')
        itemloader.add_css('company_url', '#job_company dt a::attr(href)')
        itemloader.add_value('crawl_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        job_item = itemloader.load_item()

        return job_item
