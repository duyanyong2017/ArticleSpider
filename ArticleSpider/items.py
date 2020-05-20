# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from w3lib.html import remove_tags

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_splash(value):
    return value.replace("/", "")


def handle_jobaddr(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    tags = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr)
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url,url_object_id, salary,job_city
            ,work_years,degree_need,job_type,tags,publish_time
            ,job_advantage,job_desc,job_addr,company_name,company_url
            ,crawl_time) 
            values (%s, %s, %s, %s, %s
            , %s, %s, %s, %s, %s
            , %s, %s, %s, %s, %s
            , %s)
            on duplicate key update salary=values (salary)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"], self["job_city"]
            , self["work_years"], self["degree_need"], self["job_type"], self["tags"], self["publish_time"]
            , self["job_advantage"], self["job_desc"], self["job_addr"], self["company_name"], self["company_url"]
            , self["crawl_time"]
        )

        return insert_sql, params


# class LagouHRItem(scrapy.Item):
#     # 职位信息
#     url = scrapy.Field()
#     url_object_id = scrapy.Field()
#     position_id = scrapy.Field()
#
#     title = scrapy.Field()
#     salary_bottom = scrapy.Field()
#     salary_ceil = scrapy.Field()
#     city = scrapy.Field()
#     exp_bottom = scrapy.Field()
#     exp_ceil = scrapy.Field()
#     education = scrapy.Field()
#     category = scrapy.Field()
#     pulish_time = scrapy.Field()
#     tags = scrapy.Field()
#     lure = scrapy.Field()
#     desc = scrapy.Field()
#     require = scrapy.Field()
#     location = scrapy.Field()
#
#     # 公司信息
#     company_id = scrapy.Field()
#     company_name = scrapy.Field()
#     domain = scrapy.Field()
#     stage = scrapy.Field()
#     investment_agency = scrapy.Field()
#     scale = scrapy.Field()
#     offcial_website = scrapy.Field()
