      URL  = paste0('http://txhist.centadata.com/tfs_centadata/Pih2Sln/TransactionHistory.aspx?type=1&code=',cod,'&info=basicinfo&ci=en-us')


      trHasTrans

//*[@id="OVDSUUFXQJQU"]
list(map(lambda x: re.findall('\w+', x),text))
text = response.xpath('//*[@class="trHasTrans"]/td/text()').extract()

list(map(lambda x: re.findall('[0-9M.]+', x),text))

import csv

with open('file.csv', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)

print(your_list)

text = response.xpath('//*[@class="trHasTrans"]/td/text()').extract()
list(map(lambda x: re.findall('[0-9M.]+', x),text)