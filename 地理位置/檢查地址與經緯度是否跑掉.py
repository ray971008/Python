import os
# cd = str(input('輸入檔案路徑:'))
cd = r'C:\Users\ray5547c\Desktop\地理位置'
os.chdir(cd)

import pandas as pd
import random,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.read_csv('商圈.csv', encoding="utf-8-sig")
nameslst = list(df['名稱'])
addresslst = list(df['地址'])

latlnglst=[]

for i in range(len(df)):
    latlnglst.append([float(df.iloc[i]['lat']), float(df.iloc[i]['lng'])])


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


for i in range(30):
    driver = webdriver.Chrome()
    ua = random.choice(user_agents)
    fake_ip = random.choice(fake_ips)

    # 設定 UA 與 額外 headers（用 CDP）
    _ = driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})
    _ = driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {"X-Forwarded-For": fake_ip, "Client-IP": fake_ip, "User-Agent": ua}
    })
    print(f"使用 UA: {ua} | 偽造 IP(header): {fake_ip} -> 開始抓取: {nameslst[i]}")

    url = "https://www.google.com/maps/dir/"

    driver.get(url)

    address = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@aria-label='選擇起點或點擊地圖…']")
        )
    )
    address.send_keys(addresslst[i])
        # count+=1
        # print(count)

    time.sleep(1)

    latlng = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@aria-label='選擇目的地或點擊地圖…']")
        )
    )

    # 輸入經緯度，例如 latlnglst[0] = [24.1234, 120.5678]
    latlng.send_keys(f"{latlnglst[i][0]},{latlnglst[i][1]}")

    # 按下 Enter
    address.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.close()

