# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:08:41 2023

@author: Admin
"""

import random,requests,os,re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
url = 'https://store.line.me/stickershop/product/12999/zh-Hant?from=sticker'

proxy_list = ['167.71.211.10:80','81.162.56.154:8081','198.13.54.14:80']
ip = random.choice(proxy_list)
webpage = requests.get(url, headers=HEADERS, proxies={'http':'http://'+ip})



soup = BeautifulSoup(webpage.text,'html.parser')
# print(soup)
item  = soup.find('ul',class_="mdCMN09Ul FnStickerList")
# print(item )
item2 = item.find_all('div',class_="mdCMN09LiInner FnImage")
img = re.findall('(?:https://stickershop.line-scdn.net).*\.png',str(item2))

# print(img)
count = 0
for i in img:
    count = count +1
    root = r'C:\2張家瑞\20230808\picture2'
    suffix = '.png'
    url = i
    img = requests.get(url)
    filename = os.path.join(root, str(count)+suffix)
    with open(filename,'wb') as file:
        file.write(img.content)
