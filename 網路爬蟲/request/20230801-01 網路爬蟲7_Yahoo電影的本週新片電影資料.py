# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 12:41:22 2023

@author: Admin
"""

import requests,os,csv
from bs4 import BeautifulSoup
url = 'https://movies.yahoo.com.tw/movie_thisweek.html?guccounter=1'
HEADERS =\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

data = requests.get(url,headers = HEADERS)
# print(data)
# print(data.text)


soup = BeautifulSoup(data.text,'html.parser')
item = soup.find_all('div',{'class':'release_info_text'})
print(soup)
'''
for i in item:
    name = i.find('div',{'class':'release_movie_name'}).find('a').text
    name = name.strip()
    ename = i.find('div',{'class':'en'}).find('a').text
    ename = ename.strip()
    time =  i.find('div',{'class':'release_movie_time'}).text
    time = time.replace(' ','')
    time = time.replace('\n','')
    love = i.find('div',{'class':'leveltext'}).find('span').text
    print('電影名稱:',name)
    print('英文名稱:',ename)
    print(time)
    print('期待度:',love)
    print()
'''
