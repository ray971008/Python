import pandas as pd
import random,time,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

try:
    df = pd.read_excel(r"C:\Users\ray5547c\Desktop\專案\地理位置專案\桃園市.xlsx")
except:
    df = pd.read_excel(r"C:\Users\ray5547c\Desktop\專案\地理位置專案\測試_20筆.xlsx")
    print('第一次使用')

start = input('從第幾筆開始(若從頭開始則直接按ENTER):') 
if start != '':
    position = int(start)
else:
    position = 0


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

count = position

for i in range(position,len(df)):
    # 加入 headless 模式
    ua, fake_ip = pick_ua_and_ip()

    # Chrome 選項
    options = Options()
    options.add_argument(f"user-agent={ua}")
    options.add_argument(f"--window-size=1200,1000")       # 視窗大小
    options.add_argument(f"--window-position=720,0")   # 右上角位置
    options.add_argument("--log-level=3")                # 減少 log

    driver = webdriver.Chrome(options=options)

    ua = random.choice(user_agents)
    fake_ip = random.choice(fake_ips)

    # 設定 UA 與 額外 headers（用 CDP）
    _ = driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})
    _ = driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {"X-Forwarded-For": fake_ip, "Client-IP": fake_ip, "User-Agent": ua}
    })
    print('='*10)
    print(f'第 {count} 筆')
    print(f"開始抓取: {df['store_name'][i]}")
    print(f"地址: {df['seller_address'][i]}")

    url = "https://www.google.com/maps/"
    driver.get(url)
    # 開第二個分頁 (同樣 URL)
    driver.execute_script(f"window.open('{url}');")

    # 取得所有分頁 handle
    tabs = driver.window_handles

    # 切到第一個分頁
    driver.switch_to.window(tabs[0])

    location = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@id='searchboxinput']")
        )
    )
    time.sleep(random.uniform(1,3))
    location.send_keys(df['seller_address'][i])
    searchbtn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='searchbox-searchbutton']"))
    )
    time.sleep(random.uniform(1,3))
    searchbtn.click()

    while True:
        # 初始狀態
        error_msg = ""

        # 輸入地址
        locate_address = input("輸入地址: ").strip()

        # 如果輸入 00，直接設定 df 並跳出迴圈
        if locate_address == "00":
            df.loc[i, 'latitude'] = "00"
            df.loc[i, 'longtitude'] = "00"
            df.loc[i, 'locate_address'] = "00"
            break

        # 偵測敏感關鍵字或樓層重複
        floors = re.findall(r'\d+樓', locate_address)
        if re.search(r'鄰|里', locate_address):
            error_msg += "地址中包含 '鄰' 或 '里'。\n"
        if len(floors) > 1:
            error_msg += "地址中出現多個樓層。\n"

        # 去掉開頭郵遞區號
        if re.match(r'^\d+', locate_address):
            locate_address = re.sub(r'^\d+\s*', '', locate_address)

        # 輸入經緯度
        latlng = input('輸入經緯度: ')
        pattern = r'[-+]?\d*\.\d+|\d+'
        try:
            matches = re.findall(pattern, latlng)
            latitude = float(matches[0])
            longitude = float(matches[1])
        except:
            error_msg += "經緯度格式錯誤。\n"
            latitude = longitude = None

        # 如果有任何錯誤，統一詢問是否重新輸入
        if error_msg:
            print("發現問題：\n" + error_msg)
            retry = input("是否要重新輸入? (Y/N): ").strip().upper()
            if retry != 'N':
                continue  # 回到最開始重新輸入地址
            elif retry == 'exit':
                import sys
                sys.exit("程式已結束")
            else:
                break

        # 沒有錯誤，將資料寫入 df
        df.loc[i, 'latitude'] = latitude
        df.loc[i, 'longtitude'] = longitude
        df.loc[i, 'locate_address'] = locate_address
        break

    driver.close()
    driver.switch_to.window(tabs[1])
    driver.close()
    print(f' {df['store_name'][i]} 完成!')
    df.to_excel(r"C:\Users\ray5547c\Desktop\專案\地理位置專案\桃園市.xlsx",index=False)
    count+=1
print('全部完成~')
