# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CentaPartItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Saleable_Area = Field()
    Gross_Area = Field()
    Price = Field()
    Year = Field()
    Floor = Field()
    Flat = Field()
    Phase = Field()
    Block = Field()
    Name = Field()
    bldg_code = Field()

class CentaCodeItem(Item):
    bldg_code = Field()
    flat_code = Field()
    Gross_Price_Area = Field()
    Saleable_Price_Area = Field()
    Date = Field()
    Gross_Area = Field()
    Price = Field()
    Address = Field()
    Saleable_Area = Field()