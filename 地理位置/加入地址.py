import time
import re
import pandas as pd
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('商圈.csv', encoding="utf-8-sig")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]
fake_ips = [
    "203.217.101.144",
    "122.116.125.115",
    "182.155.254.159",
    "211.73.178.144"
]

# 輔助函式：隨機選 UA 與 fake ip
def pick_ua_and_ip():
    ua = random.choice(user_agents)
    fake_ip = random.choice(fake_ips)
    return ua, fake_ip

namelst=list(df['名稱']) # 商區名稱 
hreflst=list(df['商圈網址']) # 商圈網址
addresslst=[] # 地址
mapaddresslst=[] # 定位地址
latlst = []  # 緯度
lnglst = []  # 經度
# 商圈地點
# count =0
for k in hreflst: 
    driver = webdriver.Chrome()
    ua = random.choice(user_agents)
    fake_ip = random.choice(fake_ips)

    # 設定 UA 與 額外 headers（用 CDP）
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {
            "X-Forwarded-For": fake_ip,
            "Client-IP": fake_ip,
            "User-Agent": ua
        }
    })
    # count+=1
    # print(count)
    # print(f"使用 UA: {ua} | 偽造 IP(header): {fake_ip} -> 開始抓取: {k}")

    url = k if k.startswith("http") else ("https://www.google.com/maps/place?q=" + k)
    driver.get(url)
    driver.get(k)
    time.sleep(random.randint(1,3))
    a_element = WebDriverWait(driver, 30).until(  # 最大等 30 秒，但如果早就出現會立即返回
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.font-semibold"))
    )
    soup2 = BeautifulSoup(driver.page_source,'html.parser')
    address = soup2.select('p.font-semibold')[1].text
    # mapaddress = soup2.find("div", {"class": "place-card place-card-large"})
    # iframe = driver.find_element(By.TAG_NAME, "iframe")
    # driver.switch_to.frame(iframe)
    # soup_iframe = BeautifulSoup(driver.page_source, "html.parser")
    # text = soup_iframe.prettify()

    # match = re.search(r'"\w+:0x[0-9a-f]+","([^"]+)",\[(\d+\.\d+),(\d+\.\d+)\]', text)
    # if match:
    #     mapaddress = match.group(1)
    #     lat = match.group(2)
    #     lng = match.group(3)
    #     print(address,mapaddress, lat, lng,end='\n\n')
    # # mapaddress = soup_iframe.find("div", {"class": "place-card place-card-large"})
    # driver.switch_to.default_content()
    # time.sleep(random.randint(1,3))
    # addresslst.append(address)
    # mapaddresslst.append(mapaddress)
    # latlst.append(lat)
    # lnglst.append(lng)
    driver.close()

    position = hreflst.index(k)
    if position % 10 ==0:
        print(f'商圈經緯度已完成 {position} 筆',end='/n')
print(f'商圈地點結束')
mapaddresslst =[
    re.sub(r'^\d+\s*', '', addr) if isinstance(addr, str) else addr
    for addr in mapaddresslst
]
df['地址']=addresslst
# df['地圖定位地址']=mapaddresslst
# df['lat']=latlst
# df['lng']=lnglst

df = df[['名稱', '地址']]

df.to_csv('商圈.csv', index=False, encoding="utf-8-sig")


