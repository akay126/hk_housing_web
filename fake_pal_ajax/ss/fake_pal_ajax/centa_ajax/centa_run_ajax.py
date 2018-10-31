import pandas as pd
import csv
import centa_ajax as cj


df_rm = pd.read_csv('df_rm.csv')
columns ={'Gross_Price_Area', 'Saleable_Price_Area', 'Date', 'Gross_Area','Price', 'Address', 'Saleable_Area', 'bldg_code', 'flat_code'}
with open('Centa_ajax.csv', 'w', encoding='utf-8') as csvfile:
    review_writer = csv.writer(csvfile)
    review_writer.writerow(columns)
    for i in range(len(df_rm)):
        df_his = cj.centa_ajax(df_rm['bldg_code'].iloc[i], df_rm['flat_code'].iloc[i])
        for j in range(len(df_his)):
            item= {}       
            item['Saleable_Area'] = df_his.iloc[j]['Saleable_Area']
            item['Gross_Area'] = df_his.iloc[j]['Gross_Area']
            item['bldg_code'] = df_rm['bldg_code'].iloc[i]
            item['Address'] = df_his.iloc[j]['Address']
            item['Date'] = df_his.iloc[j]['Date']
            item['Gross_Price_Area'] = df_his.iloc[j]['Gross_Price_Area']           
            item['flat_code'] = df_rm['flat_code'].iloc[i]
            item['Saleable_Price_Area'] = df_his.iloc[j]['Saleable_Price_Area']
            item['Price'] = df_his.iloc[j]['Price']
            review_writer.writerow(item.values())
        print (i)
df = pd.read_csv('Centa_ajax.csv')
df.to_csv('Centa_ajax.csv',index = False)
print ('Done!!!')