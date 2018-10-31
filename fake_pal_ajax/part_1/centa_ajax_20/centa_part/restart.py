import pandas as pd

def restart (list_dl):

    df = pd.read_csv('ss/Centa_Part.csv')
    df.to_csv('ss/Centa_Part.csv',index=False)
    list_done = df['flat_code']
    list_done = list(list_done)
    rem = list(set(list_dl) - set(list_done))
    request_urls = ['http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code={}&info=basicinfo&ci=en-us'.format(i) for i in rem]
    
    return request_urls

    