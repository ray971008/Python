# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 09:59:31 2023

@author: Admin
"""

import requests,time,os
url = 'https://18read.net/book/chapter/10770'+'236'
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
data = requests.get(url,headers =HEADERS )

os.chdir(r'C:\2張家瑞\20230802')
# print('網址: ',url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(data.text,'html.parser')
item1 = soup.find_all('div',class_='bookbody')
# print(item)
for i in item1:
    title = i.find('h2').find('em').text
    # print(title)
    index = i.find('h2').text
    
with open(title+'- novel.txt','wt',encoding='utf-8') as file: 
    file.write(title)

    
for i in range(5):

    
    url = 'https://18read.net/book/chapter/10770'+str(236+i)
    HEADERS = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    data = requests.get(url,headers =HEADERS )
    
    
    
    soup = BeautifulSoup(data.text,'html.parser')
    item1 = soup.find_all('div',class_='bookbody')
    # print(item)
    for i in item1:
        # print(title)
        index = i.find('h2').text
        index = '\n'+index + '\n'
    with open(title+'- novel.txt','at',encoding='utf-8') as file: 
        file.write('\n')
        file.write(index)
    
    item2 = soup.find('div',class_='novelcontent')
    content = item2.find_all('p')
    # print(content.get_text())
    all_content = ''
    for i in range(len(content)-1):
        all_content = all_content + content[i].text.replace(content[i+1].text,'\n')

    all_content = all_content + content[-1].text
        # print(content)
        
    with open(title+'- novel.txt','at',encoding='utf-8') as file:
        file.write('\n')  
        file.write(all_content)
              
        
    time.sleep(10)