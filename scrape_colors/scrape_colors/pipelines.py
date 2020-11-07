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

        sql = "show tables"
        self.cursor.execute(sql)
        table = self.cursor.fetchone()
        if table:
            self.cursor.execute("DROP TABLE palette")
            self.connection.commit()

        sql = "CREATE TABLE palette (id int, color1 varchar(32), color2 varchar(32), color3 varchar(32), color4 varchar(32), color5 varchar(32), foundcolor boolean)"
        self.cursor.execute(sql)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        sql = "INSERT INTO palette values (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(
            sql,
            (
                item["id"],
                item["color1"],
                item["color2"],
                item["color3"],
                item["color4"],
                item["color5"],
                item["foundcolor"],
            ),
        )
        self.connection.commit()

        return item
