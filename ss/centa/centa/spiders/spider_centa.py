from scrapy import Spider
from centa.items import CentaItem
import csv


class BestBuySpider(Spider):
    name = 'centa_spider'
    allowed_urls = ['http://www1.centadata.com/']
    start_urls = ['http://www1.centadata.com/epaddresssearch1.aspx?type=district16&code=HK']
    def parse(self, response):
        region = ['HK','KL','NE','NW']
        request_urls = ['http://www1.centadata.com/epaddresssearch1.aspx?type=district16&code={}'.format(i) for i in region ]
        r_1 = response.xpath('//*[@title="Properties in District"]/tr/@onclick').extract()
        
        for url in request_urls:
            yield Request(url=url, callback=self.parse_dist_page)

    def parse_dist_page(self,response):
        #District Page get Java ref javascript:jsfreloadthis5('district17','117','','','0');
        d_1 = response.xpath('//*[@title="Properties in District"]/tr/@onclick').extract()
        d_1 = list(map(lambda x: x.replace('javascript:jsfreloadthis5(',''),d_1))
        d_1 = list(map(lambda x: x.replace("'",''),d_1))
        d_1 = list(map(lambda x: x.replace(')',''),d_1))
        d_1 = list(map(lambda x: x.replace(';',''),d_1))
        d_1 = list(map(lambda x: x.split(',')[:2],d_1))
        request_urls = ['http://www1.centadata.com/epaddresssearch1.aspx?type={}&code={}&info=&code2=&page=0'.format(i[0],i[1]) for i in d_1]



        for url in request_urls:
            yield Request(url=url, meta={'d_1' = d_1}callback=self.parse_bldg_page)
    
    def parse_bldg_page(self,response):

        d_1 = response.meta['d_1']

        pages = response.xpath('//*[@id="Form2"]/table[3]/tr/td[2]/text()').extract()
        pages = int(pages[0].replace('Page 1 of ',''))

        request_urls = ['http://www1.centadata.com/epaddresssearch1.aspx?type={district17}&code={101}&info=&code2&page=0'.format(i[0],i[1]) for i in range(pages+1)]
        
        response.xpath('//*[@title="Transaction Records"]/tr/@onclick').extract()

        



                for url in request_urls:
            yield Request(url=url, callback=self.parse_bldg_page)

