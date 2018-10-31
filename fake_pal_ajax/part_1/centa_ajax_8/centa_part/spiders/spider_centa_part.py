from scrapy import Spider, Request
from centa_part.items import  CentaCodeItem
import centa_part.centa_ajax as cj
import csv
from centa_part.restart import restart
import pandas as pd
from numpy import repeat,array

class CentaPartSpider(Spider):
    name = 'spider_centa_part'
    allowed_urls = ['http://txhist.centadata.com/']
    start_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code=SSPPWSPEPS&info=basicinfo&ci=en-us']
    def parse(self, response):
        bldg_code = pd.read_csv('bldg_code.csv')
        bldg_code = bldg_code['bldg_code']
        request_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code={}&info=basicinfo&ci=en-us'.format(i) for i in bldg_code]
        
        for url,dl in zip(request_urls,bldg_code):
            yield Request(url=url, meta = {'dl': dl},callback=self.parse_indv)
    
    def parse_indv(self, response):
        dl = response.meta['dl']

        list_indv = response.xpath('//*[@class="unitTran-main-table-td"]/table/tr/@id').extract()
        
        for i in range(len(list_indv)):
            df_his = cj.centa_ajax(dl, list_indv[i]) # history of data frames
            for j in range(len(df_his)):
                item2= CentaCodeItem()
                item2['Gross_Price_Area'] = df_his.iloc[j]['Gross_Price_Area']
                item2['Saleable_Price_Area'] = df_his.iloc[j]['Saleable_Price_Area']
                item2['Date'] = df_his.iloc[j]['Date']
                item2['Gross_Area'] = df_his.iloc[j]['Gross_Area']
                item2['Price'] = df_his.iloc[j]['Price']
                item2['Address'] = df_his.iloc[j]['Address']
                item2['Saleable_Area'] = df_his.iloc[j]['Saleable_Area']
                item2['bldg_code'] = dl
                item2['flat_code'] = list_indv[i]
                yield item2
