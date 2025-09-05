# 套件
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time,re,random,os

def dcard(count,url,csv_name):
    # 開一個 chrome 視窗
    browser = webdriver.Chrome()

# 設定 chrome
chromeOptions = webdriver.ChromeOptions()

browser.get(url)
time.sleep(5)

# 轉成文字檔 與.text的意思差不多

data_key = [] # 網站爬蟲使用的定位
publish_time_col = [] # 文章發文時間
title_col = []  # 文章開頭
introduction_col = [] # 文章簡介
content_col=[] # 文章內容
herf_col = [] # 文章網址

# 輸入爬文章數

for i in range(count):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    item1 = soup.find('div', attrs={'data-key': str(i)})
    title = item1.find('a')
    introduction = item1.find('div', class_="atm_d2_1gzgpud atm_ks_15vqwwr m16n7y82")
    herf = str(item1.find('a'))
    if (title!=None) and (introduction!=None):
        title = title.text.replace('\n', ' ')
        #print(title)

        introduction = introduction.text
        herf = re.findall('href="(.*)" style="',herf)

        article_url ='https://www.dcard.tw'+herf[0]
        #ip = random.choice(proxy_list)
        time.sleep(2)
        driver = webdriver.Chrome()
        driver.get(article_url)
        time.sleep(2)
        soup2 =  BeautifulSoup(driver.page_source,'html.parser')
        publish_time = soup2.find('div',class_='atm_cs_741nk atm_c8_125m1w1 atm_g3_117mgzj atm_7l_1o85cey atm_vv_1q9ccgz atm_lzn0r3_af0gpl atm_du7p7_1o8liyq atm_1qszg8z_yh40bf atm_1ti0u92_1o85cey er347re')
        publish_time = re.findall('datetime="(.*:..:..).*"', str(publish_time))[0]
        publish_time = publish_time.replace('T',' ')

        # 轉換時間格式
        dateFormatter = "%Y-%m-%d %H:%M:%S"

        publish_time = datetime.strptime(publish_time, dateFormatter)
        print(publish_time)
        item2 = soup2.find('div',class_='atm_vv_1btx8ck atm_w4_1hnarqo c1ehvwc9')
        item2 = item2.find_all('span')
        txt=''
        for k in item2:
            if txt =='':
                txt = k.text
            else:
                txt = txt + k.text
        txt = txt.replace('\n',' ')

        
        driver.close()

        data_key.append(str(i))
        publish_time_col.append(publish_time)
        title_col.append(title)
        introduction_col.append(introduction)
        content_col.append(txt)
        herf_col.append(article_url)

    

    if ((i%5)==0) and (i !=count) and(i != 0):
        datakey = str(i)
        print('目前進度: 第',datakey,'篇文章')
        # 使用 WebDriverWait 等待元素的出現
        target_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@data-key="{datakey}"]'))
        )
        browser.execute_script("arguments[0].scrollIntoView();", target_element)
        time.sleep(5)
#browser.close()

dcard_df = pd.DataFrame({'data-key':data_key,
                         '發文時間':publish_time,
                         '標題':title_col,
                         '文章簡介':introduction_col,
                         '文章內容':content_col,
                         '文章網址':herf_col},
                        index = list(range(1,(len(title_col)+1))))

dcard_df.to_csv(csv_name,sep=',',index=False,header =True,encoding='UTF-8')
print("complete")
#dcard(文章數,"網址",'存檔名')
dcard(11,"https://www.dcard.tw/f/youtuber?tab=latest",'dcard 爬蟲.csv')
df = pd.read_csv('dcard 爬蟲.csv')
print(df)
a =[1,4,2]
