# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:29:18 2023

@author: Admin
"""

import requests
# from bs4 import BeautifulSoup



# payload = {'keywords': '新竹市','limit': '5'}
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
url = 'https://www.kkday.com/zh-tw/product/ajax_get_autocomplete\
_prod_data?keywords=%E6%96%B0%E7%AB%B9%E5%B8%82&limit=5'
webpage = requests.get(url,headers =HEADERS)


content = webpage.json()['data']

# print(content)
for i in content:
    name = i['name']
    price = i['price']
    print('產品: '+name,'價格: '+str(price),sep='\n')
    print()