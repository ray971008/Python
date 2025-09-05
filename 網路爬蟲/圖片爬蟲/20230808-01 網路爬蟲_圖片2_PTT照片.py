# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 10:33:48 2023

@author: Admin
"""

import random,requests,os
from bs4 import BeautifulSoup
import re

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
url = 'https://disp.cc/b/Beauty/baxQ'

proxy_list = ['167.71.211.10:80','81.162.56.154:8081','198.13.54.14:80']
ip = random.choice(proxy_list)
webpage = requests.get(url, headers=HEADERS, proxies={'http':'http://'+ip})



soup = BeautifulSoup(webpage.text,'html.parser')
# print(soup)
item  = soup.find('div',class_="text_css")
item2 = item.find_all('a',target="_blank",rel="nofollow")
# print(item)
picture = []
for i in item2:
    i = i.text
    img = re.findall('.*.gif',i)
    if img != []:
        picture.append(img[0])
# print(picture)


count = 20
for i in picture:
    count = count +1
    root = r'C:\pictures'
    suffix = '.gif'
    url = i
    img = requests.get(url)
    filename = os.path.join(root, str(count)+suffix)
    with open(filename,'wb') as file:
        file.write(img.content)
