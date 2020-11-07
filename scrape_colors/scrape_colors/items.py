# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeColorsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    color1 = scrapy.Field()
    color2 = scrapy.Field()
    color3 = scrapy.Field()
    color4 = scrapy.Field()
    color5 = scrapy.Field()
    foundcolor = scrapy.Field()
