import time
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

citycode_df = pd.read_csv('/Users/ray/Downloads/縣市代碼.csv')
city_dict = dict(zip(citycode_df["縣市名稱"], citycode_df["縣市代碼"]))
districtcode_df = pd.read_csv('/Users/ray/Downloads/鄉鎮區代碼.csv')
district_dict = dict(zip(districtcode_df["鄉鎮區名稱"], districtcode_df["鄉鎮區代碼"]))

chrome_options = webdriver.ChromeOptions()

# 直接指定 executable_path
browser = webdriver.Chrome()

url = "https://khh.travel/zh-tw/attractions/list/?category=953"
browser.get(url)

time.sleep(2)
soup = BeautifulSoup(browser.page_source,'html.parser')
item = soup.find_all('li',class_='col-12 col-md-4 col-xl-3 d-flex')
namelst=[]
hreflst=[]

for i in item:
    name = i.find('div',class_='mb-1 mb-md-2 fz-18px fz-xl-20px font-weight-bold lh-initial line-clamp-2').text
    namelst.append(name)
    href = 'https://khh.travel' + i.find('a')["href"]
    hreflst.append(href)

HEADERS ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64 ) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

addresslst=[]
citylst=[]
city_codelst=[]
districtlst=[]
district_codelst=[]
latlst=[]
lnglst=[]
for url in hreflst:
    data = requests.get(url,headers = HEADERS)
    soup = BeautifulSoup(data.text,'html.parser')
    item = soup.find('div',class_='max-w-[900px] mx-auto')
    address = item.find('span').text
    addresslst.append(address)
    match = re.match(r'(.+?[縣市])(.{1,3}[區鄉鎮市])', address)
    city = match.group(1)
    district = match.group(2) 
    citylst.append(city)    
    city_codelst.append(city_dict.get(city))
    districtlst.append(district) 
    district_codelst.append(district_dict.get(district))

    
    maphref = item.find('a',class_='d-flex align-items-center hover-secondary trs-all')["href"]
    match = re.search(r'/place/([0-9\.\-]+),([0-9\.\-]+)', maphref)
    lat = float(match.group(1))
    lng = float(match.group(2))
    latlst.append(lat)
    lnglst.append(lng)

df = pd.DataFrame({
    '縣市':citylst,
    '鄉鎮區':districtlst,
    '縣市代碼':city_codelst,
    '鄉鎮區代碼':district_codelst,
    '名稱':namelst,
    '地址':addresslst,
    'lat':latlst,
    'long':lnglst
})
df.to_csv('/Users/ray/Downloads/高雄市夜市商圈.csv', index=False, encoding="utf-8-sig")