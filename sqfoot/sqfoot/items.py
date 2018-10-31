# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SqfootItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = Field()
    date = Field()
    dist = Field()
    add = Field()
    bldg = Field()
    case = Field()