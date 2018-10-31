# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CentaPartItem(Item):
    # define the fields for your item here like:
    Address= Field()
    Complete_Date =Field()
    Total_Units = Field()
    Total_Floor =Field()
    Total_Flat = Field()
    Phase = Field()
    Block = Field()
    Name = Field()
    bldg_code = Field()
    cor_x = Field()
    cor_y = Field()    

