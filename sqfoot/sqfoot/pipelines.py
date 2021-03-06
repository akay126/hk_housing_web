# -*- coding: utf-8 -*-

# Define your item pipelines here	
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from pandas import read_csv


class SqfootPipeline(object):

    def __init__(self):
        self.filename = 'sqfoot_hkdeath.csv'

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
        print("Starting csv blank line cleaning")
        f = read_csv(self.filename)
        f.to_csv(self.filename,index=False)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
