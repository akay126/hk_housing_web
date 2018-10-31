from scrapy import Spider, Request
from centa_part.items import  CentaCodeItem
import centa_part.centa_ajax as cj
import csv
# from pandas import DataFrame,read_csv
import pandas as pd
from numpy import repeat,array

class CentaPartSpider(Spider):
    name = 'spider_centa_part'
    allowed_urls = ['http://txhist.centadata.com/']
    start_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code=SSPPWSPEPS&info=basicinfo&ci=en-us']
    def parse(self, response):
        f = open('list_dl.csv','r')
        list_dl = list(map(lambda x: x.strip(),list(f)))
        f.close()
        
        request_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code={}&info=basicinfo&ci=en-us'.format(i) for i in list_dl]
               
        for url,dl in zip(request_urls[18101:19910],list_dl):
            yield Request(url=url, meta = {'dl': dl},callback=self.parse_indv)
    
    def parse_indv(self, response):
        dl = response.meta['dl']
       

        # All Units 
        r_unit = response.xpath('//*[@id="unitTran-main-table"]/tr[2]/td/table/tr/td')

        temp = []
        for i in range(len(r_unit)):
            if i%5!=4:
                temp += [r_unit[i].xpath('./text()').extract()[0].replace(',','').strip()]
        temp_list = [temp[i:i+4] for i in range(0, len(temp), 4)]
        

        
        df_units = pd.DataFrame(temp_list,columns= ['Saleable_Area','Gross_Area','Price','Year'])

        r_unit  = response.xpath('//*[@id="tblFloor"]/tr/td/b/text()').extract()
        r_unit =list(map(lambda x: x.strip(),r_unit)) 

        # Flats
        r_Flat = response.xpath('//*[@id="unitTran-main-table"]/tr[1]/td/b/text()').extract()
        r_Flat =list(map(lambda x: x.strip(),r_Flat))
        r_Flat = [x for x in r_Flat if x!='']
        r_Flat = repeat(array(r_Flat), [len(r_unit)], axis=0)

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
        
         ## Combine Time
        df_units['Floor'] = r_unit * int(len(df_units)/len(r_unit))
        df_units['Flat'] = r_Flat 
        df_units['Phase'] = r_phase
        df_units['Block'] =r_block 
        df_units['Name'] =r_name         

        list_indv = response.xpath('//*[@class="unitTran-main-table-td"]/table/tr/@id').extract()
        
        # for i in range(len(df_units)):
        #     item = CentaPartItem()            
        #     item['Saleable_Area'] =df_units.iloc[i]['Saleable_Area']
        #     item['Gross_Area'] = df_units.iloc[i]['Gross_Area']
        #     item['Price'] = df_units.iloc[i]['Price']
        #     item['Year'] = df_units.iloc[i]['Year']
        #     item['Floor'] = df_units.iloc[i]['Floor']
        #     item['Flat'] = df_units.iloc[i]['Flat']
        #     item['Phase'] = df_units.iloc[i]['Phase']
        #     item['Block'] = df_units.iloc[i]['Block']
        #     item['Name'] = df_units.iloc[i]['Name']
        #     item['bldg_code'] = dl
        #     yield item

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
