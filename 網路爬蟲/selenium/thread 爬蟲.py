import time,random,os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

df = pd.DataFrame(columns=['keyword','作者','日期','內文','按讚數','評論數','轉發數','分享數'])

searchwordlst=[]
for i in range(17,9,-1):
    searchwordlst.append('iphone'+str(i))

for searchword in searchwordlst:
    proxy_list = ['20.27.15.49','64.92.82.61']
    ip = random.choice(proxy_list)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server=http://{ip}")

    # 直接指定 executable_path
    browser = webdriver.Chrome()

    url = "https://www.threads.com/search"
    browser.get(url)

    # 等 input 出現
    search = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input"))
    )

    time.sleep(5)
    search = browser.find_element(By.XPATH,"//input")
    time.sleep(5)

    search.send_keys(searchword)
    time.sleep(5)
    search.send_keys(Keys.ENTER)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    item = soup.find_all('div',class_='x78zum5 xdt5ytf')
    namelst=[]
    date_strlst=[]
    contentlst=[]
    likeslst=[]
    commentslst=[]
    reportslst=[]
    shareslst=[]

    for i in item:
        name = i.find('span').text
        namelst.append(name)
        daytime = i.find('time')
        date_str = daytime['datetime'].split("T")[0]
        date_strlst.append(date_str)
        content = i.find('div',class_='x1xdureb xkbb5z x13vxnyz').text
        contentlst.append(content)
        count = i.find_all("div", {"class": "x6s0dn4 x17zd0t2 x78zum5 xl56j7k"})

        likes = count[0].text
        likeslst.append(likes)
        comments = count[1].text
        commentslst.append(comments)
        reports = count[2].text
        reportslst.append(reports)
        shares = count[3].text
        shareslst.append(shares)

    df1 = pd.DataFrame({'keyword':f'{searchword}',
                    '作者':namelst,
                    '日期':date_strlst, 
                    '內文':contentlst,
                    '按讚數':likeslst,
                    '評論數':commentslst,
                    '轉發數':reportslst,
                    '分享數':shareslst})
    df = pd.concat([df, df1]) # 縱向合併 dataframe
    time.sleep(10)
    browser.close()
    time.sleep(5)
    print(f'{searchword} 已完成')

os.chdir('/Users/ray/Desktop')
df.to_csv("threads_data.csv", index=False, encoding="utf-8-sig")
print('dataframe儲存完成')
