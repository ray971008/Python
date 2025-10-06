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
df2 = pd.read_csv('/Users/ray/Downloads/商圈.csv', encoding="utf-8-sig")
print(df2.head())
print(df.head())
namelst=list(df2['名稱']) # 商區名稱 
hreflst=list(df2['商圈網址']) # 商圈網址
addresslst = df2['地址']

df2.to_csv('/Users/ray/Downloads/商圈.csv', index=False, encoding="utf-8-sig")

citylst=[] # 縣市
city_codelst=[] # 縣市代碼
districtlst=[] # 鄉鎮區
district_codelst=[] # 鄉鎮區代碼

count=1
for k in addresslst:
    city_match = re.match(r'(.+?[縣市])\s*(.+?[區鄉鎮市])', k)
    if city_match:
        city = city_match.group(1)
        district = city_match.group(2)
        citylst.append(city)
        districtlst.append(district)
    else:
        print(f"無法匹配的地址: {k}")
    
    # 縣市代碼搜尋
    city_code = df[df['縣市名稱'] == city]['縣市代碼'].iloc[0]
    city_codelst.append(city_code)

    district_code_series = df[(df['縣市名稱'] == city) & (df['鄉鎮區名稱'] == district)]['鄉鎮區代碼']
    if not district_code_series.empty:
        district_code = district_code_series.iloc[0]
        district_codelst.append(district_code)
    else:
        district_code_series = df[(df['縣市名稱'] == city) & (df['鄉鎮區名稱'] == district+'區')]['鄉鎮區代碼'].iloc[0]
        district_codelst.append(district_code)
    print(f'地點代碼結束')

df2['縣市']=citylst
df2['鄉鎮區']=districtlst
df2['縣市代碼']=city_codelst
df2['鄉鎮區代碼']=district_codelst
df2 = df2[['縣市', '鄉鎮區', '縣市代碼', '鄉鎮區代碼', '名稱', '地址','地圖定位地址', 'lat','lng','商圈網址']]

df2.to_csv('/Users/ray/Downloads/商圈.csv', index=False, encoding="utf-8-sig")