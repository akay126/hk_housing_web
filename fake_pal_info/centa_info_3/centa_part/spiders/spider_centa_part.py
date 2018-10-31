from scrapy import Spider, Request
from centa_part.items import CentaPartItem
import csv
import re
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

        ## Get info for building r_info1 is first column
        r_info1 = response.xpath('//*[@id="tblBodyContent"]/tr[4]/td[2]/table/tr[1]/td[3]/table[2]/tr/td[1]/text()').extract()
        r_info1 =list(map(lambda x: x.strip(),r_info1))
        r_info1 = [x for x in r_info1 if x!='']

        r_info = response.xpath('//*[@id="tblBodyContent"]/tr[4]/td[2]/table/tr[1]/td[3]/table[2]/tr/td[2]/text()').extract()
        r_info =list(map(lambda x: x.strip(),r_info))
        r_info = [x for x in r_info if x!='']

        ## Get cori
        r_cor = response.xpath('.//*[@id="tblBodyContent"]/tr[4]/td[2]/table/tr/td[1]/div/table/tr[1]/td/a/@href').extract_first()
        r_cor = re.findall('\d\d\d\d\d\d',r_cor)

        item = CentaPartItem()
        if len(r_info1)==5:
            item['Address'] = ""
            item['Complete_Date'] = r_info[0]
            item['Total_Units'] = r_info[1]
            item['Total_Floor'] = r_info[2]
            item['Total_Flat'] = r_info[3]
        elif len(r_info1)==6 :
            item['Address'] = r_info[0]
            item['Complete_Date'] = r_info[1]
            item['Total_Units'] = r_info[2]
            item['Total_Floor'] = r_info[3]
            item['Total_Flat'] = r_info[4]
        else:
            item['Address'] = ""
            item['Complete_Date'] = ""
            item['Total_Units'] = ""
            item['Total_Floor'] = ""
            item['Total_Flat'] = ""
        item['Phase'] = r_phase
        item['Block'] = r_block
        item['Name'] = r_name
        item['bldg_code'] = dl
        item['cor_x'] = r_cor[0]
        item['cor_y'] = r_cor[1]
        yield item
