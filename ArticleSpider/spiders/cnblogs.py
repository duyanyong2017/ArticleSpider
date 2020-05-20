# -*- coding: utf-8 -*-
from urllib import parse
import json
import re

import scrapy
from scrapy import Request
import requests

from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.utils import common


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        post_nodes = response.css("#news_list .news_block")
        for post_node in post_nodes[:1]:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            if image_url.startswith('https') == False:
                image_url = 'https:' + image_url

            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        next_url = response.css("div.pager a:last_child::text").extract_first("")
        if next_url == "Next > ":
            next_url = response.css("div.pager a:last_child::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        next_url = response.xpath("//a[contains(text(),'Next >')]/href").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            article_item = ArticlespiderItem()
            title = response.css("#news_title a::text").extract_first("")
            create_date = response.css("#news_info .time::text").extract_first("")
            match_create_date = re.match('.*?(\d+.*)', create_date)
            if match_create_date:
                create_date = match_create_date.group(1)
            content = response.css("#news_content").extract()
            tag_list = response.css(".news_tags a::text").extract()
            tags = ','.join(tag_list)
            article_item['title'] = title
            article_item['create_date'] = create_date
            article_item['content'] = content
            article_item['tags'] = tags

            if response.meta.get('front_image_url', ''):
                article_item['front_image_url'] = [response.meta.get('front_image_url', '')]
            else:
                article_item['front_image_url'] = []
            article_item['url'] = response.url

            post_id = match_re.group(1)
            # requests是同步的库，可以放在yield中
            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={'article_item': article_item},
                          callback=self.parse_nums)
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.loads(html.text)
            # fav_nums = j_data["TotalView"]
            # comment_nums = j_data["CommentCount"]

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        praise_nums = j_data['DiggCount']
        fav_nums = j_data["TotalView"]
        comment_nums = j_data["CommentCount"]
        article_item = response.meta.get('article_item', '')
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['praise_nums'] = praise_nums
        article_item['url_object_id'] = common.get_md5(article_item['url'])

        yield article_item
