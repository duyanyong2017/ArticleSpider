# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'dyy@123', 'imooc', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into cnblog_article(title,url,url_object_id,front_image_url,front_image_path,parise_num,comment_nums,fav_nums,tags,content,create_date)
            values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = list()
        params.append(item.get('title', ''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        front_image = ','.join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ''))
        params.append(item.get('parise_num', 0))
        params.append(item.get('comment_nums', 0))
        params.append(item.get('fav_nums', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1900-01-01'))
        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_inser, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_inser(self, cursor, item):
        # insert_sql = """
        #             insert into cnblog_article(title,url,url_object_id,front_image_url,front_image_path,parise_num,comment_nums,fav_nums,tags,content,create_date)
        #             values
        #             (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update parise_num=values (parise_num)
        #         """
        # params = list()
        # params.append(item.get('title', ''))
        # params.append(item.get('url', ''))
        # params.append(item.get('url_object_id', ''))
        # front_image = ','.join(item.get('front_image_url', []))
        # params.append(front_image)
        # params.append(item.get('front_image_path', ''))
        # params.append(item.get('parise_num', 0))
        # params.append(item.get('comment_nums', 0))
        # params.append(item.get('fav_nums', 0))
        # params.append(item.get('tags', ''))
        # params.append(item.get('content', ''))
        # params.append(item.get('create_date', '1900-01-01'))

        insert_sql, params = item.get_insert_sql()

        cursor.execute(insert_sql, tuple(params))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_file_path = ''
        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_url'] = image_file_path

        return item
