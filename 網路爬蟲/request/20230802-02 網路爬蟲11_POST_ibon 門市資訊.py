# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:12:38 2023

@author: Admin
"""

import requests,os
from bs4 import BeautifulSoup
import pandas as pd
os.chdir(r'/Users/ray/Downloads/python 程式檔')
url = 'https://www.ibon.com.tw/retail_inquiry_ajax.aspx'

payload = {'strTargetField': 'COUNTY','strKeyWords': '台北市'}
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

webpage = requests.post(url,data=payload,headers =HEADERS)

soup =  BeautifulSoup(webpage.text,'html.parser')
print(soup)
item = soup.find('table',class_="font16")
item2 = item.find_all('td')

'''
number = []
name = []
location = []
for i in range(0,len(item2),3):
    number.append(item2[i].text.strip())
    
for i in range(1,len(item2),3):
    name.append(item2[i].text.strip()) 
    
for i in range(2,len(item2),3):
    location.append(item2[i].text.strip()) 

grade ={number.pop(0)+'   ':number,
        name.pop(0)+'  ':name,
        location.pop(0)+'    ':location}

df = pd.DataFrame(grade)

print(df)
'''

