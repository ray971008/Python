# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:00:22 2023

@author: Admin
"""
import requests
for i in range(1,6):
    url = 'https://www.cosme.net.tw/new-reviews?page='+str(i)
    HEADERS = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    data = requests.get(url,headers =HEADERS )
    
    
    print('網址: ',url)
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data.text,'html.parser')
    
    
    item = soup.find('div',class_='uc-reviews')
    section = item.find_all('div',class_='uc-review uc-review-with-product')

    
    
    for i in range(len(section)):
        count = 1+i
        review_content = section[i].find('div',class_='review-content-container \
                                review-content-full-container')
        print(review_content)
        '''
        review_info = review_content.find('div',class_='review-info')
        author_info= review_info.find('div',class_='author-info')
        
        name = section[i].find('div',class_='author-name').text
        score = section[i].find('div',class_='author-score').text
        s = section[i].find('div',class_='author-review-status').text
        h = section[i].find('div',class_='two-line-dot uc-content-link').text
        h = h.replace(' ','')
        print('編號: ',count)
        print('心得:',h)
        print('作者:  ',name)
        print('狀態: ',s)
        print('分數: ',score)
        print()
        '''
        
    
