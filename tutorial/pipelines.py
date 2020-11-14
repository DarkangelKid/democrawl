# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from scrapy.exceptions import DropItem
from pymongo import MongoClient
import re
from datetime import datetime


class TutorialPipeline:
    def open_spider(self, spider):
        #   connect to mongo db
        db = MongoClient('192.168.2.167', 27017).CRAWLER
        self.col_article = db['articles']
        self.col_history = db['history']

        self.col_newspaper = db['newspapers']
        self.start_time = datetime.now()

        # if (spider.name == 'baomoi'):
        #   Avoid duplicate entries in MongoDB
        self.col_newspaper.create_index([(("domain", 1))], unique=True)
        self.col_article.create_index([(("baomoi_id", 1))], unique=True)

        self.new_item = 0
        self.duplicated_item = 0

    def process_item(self, item, spider):
        if (spider.name == 'baomoi'):
            original_url = item['original_url']
            domain = re.findall(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)', original_url)[0]

            newspaper = dict()
            newspaper['name'] = item['newspaper']
            newspaper['domain'] = domain
            newspaper['el_time'] = ''
            newspaper['el_content'] = ''

            try:
                self.col_newspaper.insert(newspaper)
            except:
                pass

            try:
                self.col_article.insert(dict(item))
                self.new_item += 1
            except:
                self.duplicated_item += 1
                return item

        if (spider.name == 'content'):
            pass
        return item

    def close_spider(self, spider):
        if (spider.name == 'baomoi'):
            self.col_history.insert({
                'start_time': self.start_time,
                'finished_time': datetime.now(),
                'new_item': self.new_item,
                'duplicated_item': self.duplicated_item,
            })
