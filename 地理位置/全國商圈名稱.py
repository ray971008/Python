
import time
import re
import pandas as pd
import random
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


df = pd.read_csv('/Users/ray/Downloads/縣市鄉鎮區代碼.csv', encoding="utf-8-sig")

HEADERS ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

city_total=['臺北市','新北市','基隆市','桃園市','新竹市','新竹縣',
            '苗栗縣','臺中市','彰化縣','南投縣','雲林縣',
            '嘉義市','嘉義縣','臺南市','高雄市','屏東縣',
            '宜蘭縣','花蓮縣','臺東縣',
            '澎湖縣','金門縣','連江縣']

# 存放資料的list
namelst=[] # 商區名稱 
hreflst=[] # 商圈網址
addresslst=[] # 地址
citylst=[] # 縣市
city_codelst=[] # 縣市代碼
districtlst=[] # 鄉鎮區
district_codelst=[] # 鄉鎮區代碼
latlst=[] # 緯度
lnglst=[] # 經度

for city in city_total:
    url = f'https://serv.gcis.nat.gov.tw/district/districts?city={city}'
    browser = webdriver.Chrome()
    browser.get(url)

    # 找頁數
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-type="page"]'))
    )
    time.sleep(random.randint(1,5))
    soup = BeautifulSoup(browser.page_source,'html.parser')
    page = soup.find_all('button', attrs={'data-type': 'page'})
    
    # 解決沒有商圈問題
    try:
        nodata = soup.find('div',class_='text-lg font-semibold').text
        print(f'{city}-無商圈')
        browser.close()
    except:
        # 防止只有1頁
        if len(page) ==1:
            last_page = 1
        else:
            last_page_btn = WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Last Page']"))
            )
            time.sleep(random.randint(5,10))
            last_page_btn.click()
            time.sleep(random.randint(5,10))
            ## 找最後一頁頁數
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-type="page"]'))
            )
            soup = BeautifulSoup(browser.page_source,'html.parser')
            page = soup.find_all('button', attrs={'data-type': 'page'})
            last_page = int(page[-1].text)
        browser.close()

        # 開始截取資料
        for i in range(1,last_page+1):
            url = f'https://serv.gcis.nat.gov.tw/district/districts?city={city}&page={i}'
            browser = webdriver.Chrome()

            browser.get(url)
            a_element = WebDriverWait(browser, 30).until(  # 最大等 30 秒，但如果早就出現會立即返回
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.bg-default.ring.ring-default.divide-y.divide-default.flex.flex-col.group.rounded-xl.overflow-hidden.shadow-card"))
            )
            soup = BeautifulSoup(browser.page_source,'html.parser')
            item = soup.find_all('a',class_='bg-default ring ring-default divide-y divide-default flex flex-col group rounded-xl overflow-hidden shadow-card')
            time.sleep(random.randint(1,5))

        # 商圈名稱
            for j in item:
                name = j.find('div',class_='text-2xl text-highlighted h-[2.75em] line-clamp-2').text
                namelst.append(name)
                href = 'https://serv.gcis.nat.gov.tw' + j['href']
                hreflst.append(href)
            browser.close()
        print(f'{city}-商圈名稱結束')

store_df = pd.DataFrame({
    '名稱':namelst,
    '商圈網址':hreflst
})

store_df.to_csv('/Users/ray/Downloads/商圈.csv', index=False, encoding="utf-8-sig")
