# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import os


class ScrapeColorsPipeline:
    def __init__(self):
        # Connect to mysql
        self.connection = pymysql.connect(
            host="db",
            user="ImUser",
            # user=os.environ.get("MYSQL_USER"),
            password="mk",
            db="njmk",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cursor = self.connection.cursor()

        self.counter = 0

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):

        return item
