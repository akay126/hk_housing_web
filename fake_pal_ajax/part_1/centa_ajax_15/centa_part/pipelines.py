# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from pandas import read_csv
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals



class CentaPartPipeline(object):
    
    def __init__(self):
        self.filename = 'Centa_Part.csv'

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
        f = read_csv(self.filename)
        f.to_csv(self.filename,index=False)


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

        
# def item_type(item):
#     return type(item).__name__.replace('Item','').lower()

# class MultiCSVItemPipeline(object):
#     SaveTypes = ['centapart','centacode']
#     def __init__(self):
#         dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
#         dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

#     def spider_opened(self, spider):
#         self.files = dict([ (name, open(name+'.csv','w+b')) for name in self.SaveTypes ])
#         self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
#         [e.start_exporting() for e in self.exporters.values()]


#     def spider_closed(self, spider):
#         [e.finish_exporting() for e in self.exporters.values()]
#         [f.close() for f in self.files.values()]
#         f = read_csv('centapart.csv')
#         f.to_csv('centapart.csv',index=False)
#         f = read_csv('centacode.csv')
#         f.to_csv('centacode.csv',index=False)


#     def process_item(self, item, spider):
#         what = item_type(item)
#         if what in set(self.SaveTypes):
#             self.exporters[what].export_item(item)
#         return item

        
