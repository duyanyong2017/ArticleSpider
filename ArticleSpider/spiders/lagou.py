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
from settings import BASE_DIR, LOG_FILE
from utils.common import get_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "HOST": "www.lagou.com"
    }

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20200511220303-ab8e7163-cf66-4a23-9585-ba32f85a294f; _ga=GA1.2.945093635.1589205787; LGUID=20200511220305-c692d627-00b1-4ecb-97c8-a0ca6b2340fd; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217209824677d2-0b382c957930e9-e343166-921600-172098246784c5%22%2C%22%24device_id%22%3A%2217209824677d2-0b382c957930e9-e343166-921600-172098246784c5%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; gate_login_token=12549a43464ff34371725d66ec9dede5bbb24c5fa1c3a3e7; LG_LOGIN_USER_ID=98813412374359cf40ccf19695392ac0cb8fabaf3e75e873; LG_HAS_LOGIN=1; privacyPolicyPopup=false; index_location_city=%E4%B8%8A%E6%B5%B7; _putrc=394EED22F8DFEBAB; _gid=GA1.2.666651480.1589894305; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1589297432,1589299457,1589328213,1589894305; login=true; unick=%E6%9D%9C%E5%BD%A6%E6%B0%B8; X_MIDDLE_TOKEN=122c63f5dc673be82c80c2642ddd029f; LGSID=20200520000704-02124645-1b27-4c3c-be07-7b032dbd89dc; X_HTTP_TOKEN=7359ed97d10e9b285308099851fd47db0ded6b1185; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1589908036; LGRID=20200520010716-551705d9-fd25-4a4b-92f9-9e5c5fbdd575',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    # start_urls = ['https://www.lagou.com/jobs/list_/p-city_6']
    # start_urls = ['https://www.lagou.com/jobs/6981517.html?show=31517064ea2541b2b11f29661698f07d']

    rules = (
        # 全站爬取
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    # def start_requests(self):
    #     cookies = []
    #     if os.path.exists(BASE_DIR + "\cookies\lagou.cookie") and os.path.getsize(
    #             BASE_DIR + "\cookies\lagou.cookie") > 0:
    #         cookies = pickle.load(open(BASE_DIR + "\cookies\lagou.cookie", "rb"))
    #
    #     if not cookies:
    #         from selenium import webdriver
    #         options = webdriver.ChromeOptions()
    #         options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    #         browser = webdriver.Chrome(
    #             executable_path=r"D:\softwares\chromedriver.exe"
    #             , options=options
    #         )
    #         browser.get("https://passport.lagou.com/login/login.html")
    #         browser.find_element_by_css_selector(".form_body .input.input_white").send_keys("18896738910")
    #         browser.find_element_by_css_selector(".form_body input[type='password']").send_keys("duyanyong@320324")
    #         browser.find_element_by_css_selector("div[data-view='passwordLogin'] input.btn_lg").click()
    #
    #         time.sleep(5)
    #         cookies = browser.get_cookies()
    #
    #         pickle.dump(cookies, open(BASE_DIR + "\cookies\lagou.cookie", "wb"))
    #
    #     cookie_dict = {}
    #     for cookie in cookies:
    #         cookie_dict[cookie['name']] = cookie['value']
    #
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict, headers=self.headers, meta={
    #             'dont_redirect': True,
    #             'handle_httpstatus_list': [302]
    #         })

    def parse_job(self, response):
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        file_hadler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
        file_hadler.setLevel(level=logging.DEBUG)
        file_hadler.setFormatter(formatter)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.DEBUG)
        # stream_handler.setFormatter(formatter)

        logger.addHandler(file_hadler)
        # logger.addHandler(stream_handler)

        logger.info(response.url)

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
