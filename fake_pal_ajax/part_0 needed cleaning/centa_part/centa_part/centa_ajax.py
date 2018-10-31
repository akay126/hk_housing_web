import requests
import pandas as pd
from bs4 import BeautifulSoup

def sort_table(r):
    temp = []
    for x in r[0].findAll('td'):
        a = x.get_text().replace(':','')
        a = a.replace('Sq.Ft.','')
        a = a.strip()
        temp.append(a)

    hist_add = dict(zip(temp[::2], temp[1::2]))
    hist_add

    temp = []
    for x in r[3].findAll('td'):
        a = x.get_text().replace('@','')
        a = a.replace('(Gross)','')
        a = a.replace('(Saleable)','')
        a = a.replace('M','')
        a = a.replace('$','')
        a = a.replace(',','')
        a = a.strip()
        temp.append(a)
    
    #remove percentage
    temp = [temp[x] for x in range(len(temp)) if x%5!=4 ]
    info = ['Date','Price','Saleable_Price_Area','Gross_Price_Area']

    temp_list = [temp[i:i+4] for i in range(0, len(temp), 4)]
    temp_list = list(map(lambda x: dict(zip(info,x)),temp_list))
    temp_list = list(map(lambda x: dict(x,**hist_add),temp_list))

    temp_df = pd.DataFrame(temp_list)
    temp_df.columns = temp_df.columns.str.replace('Gross Area','Gross_Area')
    temp_df.columns = temp_df.columns.str.replace('Saleable Area','Saleable_Area')
    temp_df.columns = temp_df.columns.str.replace('Property','Address')


    return (temp_df)

def replace(xml):
    replacements = {
    "&gt;" : ">",
    "&lt;" : "<"
    }
    repl_str = xml
    for char in replacements:
        repl_str = repl_str.replace(char, replacements[char])
    return repl_str




def centa_ajax(bldg_code,flat_code):
    data = 'acode={}&cblgcode={}&cci_price=&cultureInfo=English'.format(flat_code,bldg_code)
    ref = "http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1^&code={}^&info=basicinfo^&ci=en-us".format(bldg_code)
    xml = requests.post("http://txhist.centadata.com/tfs_centadata/Pih2Sln/Ajax/AjaxServices.asmx/GenTransactionHistoryPinfo",
    data=data,
    headers={
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://txhist.centadata.com",
        "Referer": ref,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    },
    cookies={
        "ASP.NET_SessionId": "dp0nep55xt0ple45akavl545",
        "Hm_lpvt_ead590637b73af1b8bfba9fed484517e": "1539826155",
        "Hm_lvt_ead590637b73af1b8bfba9fed484517e": "1539826155",
        "__utma": "140476022.1564193495.1538496429.1538801502.1539826156.4",
        "__utmc": "140476022",
        "__utmz": "140476022.1538801502.3.3.utmcsr=hk.centadata.com^|utmccn=(referral)^|utmcmd=referral^|utmcct=/",
        "_ga": "GA1.2.1564193495.1538496429",
        "_gid": "GA1.2.1409523291.1539812569",
        "ci": "en-us"
    },
)
    xml = replace(xml.text)
    soup = BeautifulSoup(xml)
    r = soup.find(style="vertical-align:top;").findAll('table')
    return (sort_table(r))
