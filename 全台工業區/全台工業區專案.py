import pandas as pd
import random,time,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
os.chdir(r"C:\Users\ray5547c\Desktop\全臺工業區\定位")
while True:
    load_filename = input('輸入讀取檔案名稱:')

    # 檢查檔案是否存在
    if not os.path.exists(load_filename):
        print('檔案不存在，請重新輸入。')
        continue

    try:
        # 根據副檔名自動選擇讀取方式
        if load_filename.lower().endswith('.csv'):
            df = pd.read_csv(load_filename, encoding='utf-8-sig',low_memory=False)
            print('成功讀取 CSV 檔！')

        elif load_filename.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(load_filename,low_memory=False)
            print('成功讀取 Excel 檔！')

        else:
            print('不支援的副檔名，請使用 .csv 或 .xlsx。')
            continue
        break

    except Exception as e:
        print(f'發生錯誤：{e}')
        print('請重新輸入。')

save_filename = input('輸入儲存檔案的名稱:')

if 'note' not in df.columns:
    df['note'] = ''
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
    options.add_argument(f"--window-size=1000,800")       # 視窗大小
    options.add_argument(f"--window-position=550,0")   # 右上角位置
    options.add_argument("--log-level=3")                # 減少 log

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Network.enable", {})  # 確保 Network domain 啟用
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {
            "User-Agent": ua
        }
    })
    print('='*10)
    print(f'第 {count} 筆')
    print(f"開始抓取: {df['工業區名稱'][i]}")
    print(f"縣市: {df['縣市'][i]}")
    print(f"note: {df['note'][i]}")

    mapurl = 'https://www.google.com/maps/'
    # 開第一個分頁 (google map URL)
    driver.get(mapurl)

    # # 開第二個分頁 (google map URL)
    # driver.execute_script(f"window.open('{mapurl}');")

    # # 取得所有分頁 handle
    # tabs = driver.window_handles

    # # 切到第二個分頁
    # driver.switch_to.window(tabs[1])

    # location = WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, "//input[@id='searchboxinput']")
    #     )
    # )
    # # time.sleep(random.uniform(1,3))
    # location.send_keys(f'{df['緯度'][i]},{df['經度'][i]}')
    # searchbtn1 = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[@id='searchbox-searchbutton']"))
    # )
    # time.sleep(random.uniform(1,3))
    # searchbtn1.click()

    # # 切到第一個分頁
    # driver.switch_to.window(tabs[0])

    location = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@id='searchboxinput']")
        )
    )
    # time.sleep(random.uniform(1,3))
    location.send_keys(df['工業區名稱'][i])
    searchbtn2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='searchbox-searchbutton']"))
    )
    time.sleep(random.uniform(1,3))
    searchbtn2.click()

    while True:
        # 初始狀態
        error_msg = ""
        
        # 輸入地址
        locate_address = input("輸入地區: ").strip()

        # 如果輸入 00，直接設定 df 並跳出迴圈
        if locate_address == "00":
            latitude = "00"
            longitude= "00"
            locate_address = "00"
            URL = "00"
            print('經緯度: 00,00')
            note = input("是否有備註? (Y/N): ").strip()
            if note == 'Y':
                note = input('輸入備註:').strip()
            else:
                note = None
            df.loc[i, '地址'] = locate_address   
            df.loc[i, '緯度'] = latitude
            df.loc[i, '經度'] = longitude
            df.loc[i, '街景URL'] = URL
            df.loc[i, 'note'] = note
            break

        # 偵測敏感關鍵字或樓層重複
        floors = re.findall(r'\d+號', locate_address)
        if re.search(r'鄰|里|樓', locate_address):
            error_msg += "地址中包含 '鄰' 、 '里'或 '樓'。\n"
        if len(floors) > 1:
            error_msg += "地址中出現多個號碼。\n"

        # 去掉開頭郵遞區號
        if re.match(r'^\d+', locate_address):
            locate_address = re.sub(r'^\d+\s*', '', locate_address)


        # # 輸入經緯度
        # latlng = input('輸入經緯度: ')

        # try:
        #     pattern = r'[-+]?\d*\.\d+|\d+'
        #     matches = re.findall(pattern, latlng)
        #     latitude = float(matches[0])
        #     longitude = float(matches[1])
        # except:
        #     error_msg += "經緯度格式錯誤。\n"
        #     latitude = longitude = None

        # 輸入經緯度
        URL = input('輸入URL: ')
        try:
            # 尋找「@」後面接經緯度的部分
            match = re.search(r'@([-+]?\d+\.\d+),([-+]?\d+\.\d+)', URL)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
            else:
                error_msg = "網址中找不到經緯度。"
                latitude = longitude = None
        except Exception as e:
                error_msg = f"經緯度解析錯誤：{e}"
                latitude = longitude = None

        note = input("是否更改備註? (Y/N): ").strip()
        
        if note == 'Y':
            note = input('輸入備註:').strip()
        else:
            note = df.loc[i, 'note']
        # 如果有任何錯誤，統一詢問是否重新輸入
        if error_msg:
            print("發現問題：\n" + error_msg)
            retry = input("是否要重新輸入? (Y/N): ").strip().upper()
            if retry != 'N':
                continue  # 回到最開始重新輸入地址
            else:
                df.loc[i, '地址'] = locate_address
                df.loc[i, '緯度'] = latitude
                df.loc[i, '經度'] = longitude
                df.loc[i, '街景URL'] = URL
                df.loc[i, 'note'] = note
                break

        # 沒有錯誤，將資料寫入 df
        df.loc[i, '地址'] = locate_address
        df.loc[i, '緯度'] = latitude
        df.loc[i, '經度'] = longitude
        df.loc[i, '街景URL'] = URL
        df.loc[i, 'note'] = note
        break
    driver.close()
    print(f' {df['工業區名稱'][i]} 完成!')

    df.to_csv(save_filename, index=False, encoding='utf-8-sig')

    if count %10 == 0:
        exit = input("*"*3 +"是否繼續?(Y/N): ").strip().upper()
        if  exit  == 'N':
            import sys
            sys.exit("程式已結束")
    count+=1
print('全部完成~')
