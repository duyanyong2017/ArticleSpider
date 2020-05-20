from scrapy.cmdline import execute

import sys
import os

# 项目根目录添加到python路径中，防止import出错
# print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "lagou"])
# import sys
#
# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# print(sys.path.insert(0, os.path.join(BASE_DIR, 'ArticleSpider')))
#
# print(BASE_DIR)

# from settings import BASE_DIR
#
# print(BASE_DIR + "/cookies/lagou.cookie")
# import fake_useragent
#
#
# def get_header():
#     location = os.getcwd() + '/fake_useragent.json'
#     ua = fake_useragent.UserAgent(path=location, verify_ssl=False, cache=False, use_cache_server=False)
#     return ua.random
#
#
# if __name__ == '__main__':
#     get_header()
# import logging
#
# logger = logging.getLogger()
# logger.setLevel(level=logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
#
# from settings import LOG_FILE
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
# logger.debug('debug级别，一般用来打印一些调试信息，级别最低')
# logger.info('info级别，一般用来打印一些正常的操作信息')
# logger.warning('waring级别，一般用来打印警告信息')
# logger.error('error级别，一般用来打印一些错误信息')
# logger.critical('critical级别，一般用来打印一些致命的错误信息，等级最高')
