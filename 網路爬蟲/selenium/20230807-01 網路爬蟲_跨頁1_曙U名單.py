# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 10:45:55 2023

@author: Admin
"""

from selenium import webdriver
import time,random
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
chromeOptions = webdriver.ChromeOptions()

url = "https://tw.eztable.com/search"
HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
proxy_list = ['167.71.211.10:80','81.162.56.154:8081','198.13.54.14:80']
ip = random.choice(proxy_list)

chromeOptions.add_argument(f"--proxy-server=http://{ip}")


browser.get(url)
time.sleep(3)
for i in range(2):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    
#轉成文字檔 與.text的意思差不多
soup = BeautifulSoup(browser.page_source,'html.parser')
# print(soup)

item1 = soup.find('div',class_='SearchResult__StyledContainer-alt2vy-1 vlRon')
item2 = item1.find_all('div',class_='SearchResult__StyledRestaurantContent-alt2vy-4 ydffj')

for i in item2:
    nam = i.find('h2',class_='SearchResult__StyledName-alt2vy-7 kjEOTT')
    name = nam.find('a').text
    print(name)
    price = i.find('div',class_='SearchResult__StyledPrice-alt2vy-13 ghERpV').text
    print('價格: ',price)
    print()
