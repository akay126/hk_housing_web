from scrapy import Spider, Request
from centa_part.items import CentaPartItem
import csv
# from pandas import DataFrame,read_csv
import pandas as pd
from numpy import repeat,array

class CentaPartSpider(Spider):
    name = 'spider_centa_part'
    allowed_urls = ['http://txhist.centadata.com/']
    start_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code=SSPPWSPEPS&info=basicinfo&ci=en-us']
    def parse(self, response):
        bldg_code = pd.read_csv('list_dl.csv')
        bldg_code = bldg_code['bldg_code']
        request_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code={}&info=basicinfo&ci=en-us'.format(i) for i in bldg_code]
               
        for url,dl in zip(request_urls,bldg_code):
            yield Request(url=url, meta = {'dl': dl},callback=self.parse_indv)
    
    def parse_indv(self, response):
        dl = response.meta['dl']

        # Building names
        ## Phase
        head_bldg = response.xpath('//*[@class="aMenuName"]/text()').extract()
        r_name = response.xpath('//*[@id="spnMenuLast"]/text()').extract_first()

        if len(head_bldg) == 3 : # type 3
            r_phase = head_bldg[1]
            r_block = head_bldg[2]
        elif len(head_bldg)==2:
            r_phase = head_bldg[1]
            r_block = head_bldg[1]
        else:
            r_phase = r_name
            r_block = r_name


        r_info = response.xpath('//*[@id="tblBodyContent"]/tr[4]/td[2]/table/tr[1]/td[3]/table[2]/tr/td[2]/text()').extract()
        r_info =list(map(lambda x: x.strip(),r_info))
        r_info = [x for x in r_info if x!='']

        item = CentaPartItem()            
        item['Address'] = r_info[0]
        item['Complete_Date'] = r_info[1]
        item['Total_Units'] = r_info[2]
        item['Total_Floor'] = r_info[3]
        item['Total_Flat'] = r_info[4]
        item['Phase'] = r_phase
        item['Block'] = r_block
        item['Name'] = r_name
        item['bldg_code'] = dl
        yield item
