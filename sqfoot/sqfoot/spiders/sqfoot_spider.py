from scrapy import Spider, Request
from sqfoot.items import SqfootItem
import re

class SqfootSpider(Spider):
    name = 'sqfoot_spider'
    allowed_urls = ['https://www.squarefoot.com.hk']
    start_urls = ['https://www.squarefoot.com.hk/haunted/?page=0']

    def parse(self, response):

        result_urls = ['https://www.squarefoot.com.hk/haunted/?page={}'.format(x) for x in range(0,26)]

        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        print("^"*100)
        a = response.xpath('//*[@bgcolor="#EEEEEE"]/td')    
        for i in range(int(len(a)/6)):

            #year CONTAINS HREF
            year = a[6*i].xpath('./a/text()').extract_first()
            #date
            date = a[6*i+1].xpath('./text()').extract_first()
            date = '%s-%s' %(date,year)
            # district CONTAIN HREF
            dist = a[6*i+2].xpath('./a/text()').extract_first()
            #address cd
            add = a[6*i+3].xpath('./text()').extract_first()
            # Building  MAY CONTAIN HREF
            if len(a[6*i+4].xpath('./text()').extract()) == 1:
                bldg = a[6*i+4].xpath('./text()').extract()
                bldg = list(map(lambda x: x.replace('\n',''),bldg))
                bldg = list(map(lambda x: x.replace('\t',''),bldg))
                bldg = list(map(lambda x: x.strip(),bldg))[0]
            else:
                bldg = a[6*i+4].xpath('./a/text()').extract()
                bldg = list(map(lambda x: x.replace('\n',''),bldg))
                bldg = list(map(lambda x: x.replace('\t',''),bldg))
                bldg = list(map(lambda x: x.strip(),bldg))[0]
            # case
            case = a[6*i+5].xpath('./text()').extract_first()

            print("="*100)

            item = SqfootItem()
            item['year'] = year
            item['date'] = date
            item['dist'] = dist
            item['add'] = add
            item['bldg'] = bldg
            item['case'] = case            
            yield item

        b = response.xpath('//*[@bgcolor="#ffffff"]/td')   

        for i in range(int(len(b)/6)):

            #year CONTAINS HREF
            year = b[6*i].xpath('./a/text()').extract_first()
            #date
            date = b[6*i+1].xpath('./text()').extract_first()
            date = '%s-%s' %(date,year)
            # district CONTAIN HREF
            dist = b[6*i+2].xpath('./a/text()').extract_first()
            #address 
            add = b[6*i+3].xpath('./text()').extract_first()
            # Building  MAY CONTAIN HREF
            if len(b[6*i+4].xpath('./text()').extract()) == 1:
                bldg = b[6*i+4].xpath('./text()').extract()
                bldg = list(map(lambda x: x.replace('\n',''),bldg))
                bldg = list(map(lambda x: x.replace('\t',''),bldg))
                bldg = list(map(lambda x: x.strip(),bldg))[0]

            else:
                bldg = b[6*i+4].xpath('./a/text()').extract()
                bldg = list(map(lambda x: x.replace('\n',''),bldg))
                bldg = list(map(lambda x: x.replace('\t',''),bldg))
                bldg = list(map(lambda x: x.strip(),bldg))[0]
            # case
            case = b[6*i+5].xpath('./text()').extract_first()
            print("*"*50)

            item = SqfootItem()
            item['year'] = year
            item['date'] = date
            item['dist'] = dist
            item['add'] = add
            item['bldg'] = bldg
            item['case'] = case
            yield item

        

