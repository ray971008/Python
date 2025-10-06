import random
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

df = pd.read_csv('/Users/ray/Downloads/商圈.csv', encoding="utf-8-sig")
addresslst = df['地址']
latlst = []  # 緯度
lnglst = []  # 經度
print(df.head())
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

# 清理後的 fake IP（log 顯示這四個都有成功，所以全部保留）
fake_ips = [
    "203.217.101.144",
    "122.116.125.115",
    "182.155.254.159",
    "211.73.178.144"
]

def get_random_headers():
    ua = random.choice(user_agents)
    fake_ip = random.choice(fake_ips)
    headers = {
        "User-Agent": ua,
        "X-Forwarded-For": fake_ip,  # 模擬來源 IP
        "Client-IP": fake_ip
    }
    return headers , ua, fake_ip
count = 0
# 範例爬取
for k in addresslst:
    headers, ua, fake_ip = get_random_headers()
    count+=1
    print(count)
    print(f"使用 UA: {ua} | 偽造 IP: {fake_ip}")  # 印出本次使用的 UA 與 IP

    url = "https://www.google.com/maps/place?q=" + k
    response = requests.get(url, headers=headers)

    time.sleep(random.randint(1,3))
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.prettify()
    # 存成 txt
    with open(f"{'/Users/ray/Desktop/地址經緯度/'+k}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # latlng_match = re.search(r';window\.APP_INITIALIZATION_STATE=\[\[\[[-\d\.]+,([-\d\.]+),([-\d\.]+)\]', text)
    pattern = r'\[null,null,([0-9\.\-]+),([0-9\.\-]+)\]'
    latlng_match = re.search(pattern,text)
    if latlng_match:
        lat = latlng_match.group(1)
        lng = latlng_match.group(2)
    else:
        lat, lng = None, None
    print(lng,lat)
    latlst.append(lat)
    lnglst.append(lng)

    print(k+ ' : ', lat, lng,sep='\n',end='\n\n')


df['lat']=latlst
df['lng']=lnglst
df = df[['縣市', '鄉鎮區', '縣市代碼', '鄉鎮區代碼', '名稱', '地址', 'lat','lng','地圖定位地址', '商圈網址']]
df.to_csv('/Users/ray/Downloads/商圈.csv', index=False, encoding="utf-8-sig")