# -*- coding: utf-8 -*-
import os
import pickle
import time
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import selenium

from settings import BASE_DIR
from items import LagouJobItemLoader, LagouJobItem
from utils.common import get_md5


class LagouHrSpider(scrapy.Spider):
    name = 'lagou_hr'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/7146434.html']
    # -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    def parse(self, response):
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
