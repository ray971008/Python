# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:44:38 2023

@author: Admin
"""

import requests
from bs4 import BeautifulSoup



HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

url = 'https://www.booking.com/hotelfeaturedreviews/tw/hanshe.zh-tw.html?aid=376396&label=booking-name2-yefrPbbyS%2AFIINHgyCnmNgS411022708271%3Apl%3Ata%3Ap1%3Ap22%2C563%2C000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9040379%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt1O4nYvDr1lms&sid=6f80822c6d81e8df4f327b94ffd6d6bc&dest_id=-2637882;dest_type=city;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1690963080;srpvid=6a123803c0320459;type=total;ucfs=1&&_=1690965378059'
webpage = requests.get(url, headers=HEADERS)


soup =  BeautifulSoup(webpage.text,'html.parser')
# print(soup)
item = soup.find_all('div',class_='review_item_review_content')
# print(item)
# print(item)
count = 0
for i in item:
    count = count +1
#     # print('顧客: '+str(count),'評語: ',i.text,sep = '\n')
    # print('顧客: '+str(count))
    if i.find('p',class_='review_pos') != None:
        pos = i.find('p',class_='review_pos').text.strip()
        print('正評: ',pos)
    if i.find('p',class_='review_neg') != None: 
        neg = i.find('p',class_='review_neg').text
        print('負評: ',neg)
    print()



